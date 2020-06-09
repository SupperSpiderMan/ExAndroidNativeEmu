import logging
import os
import sys
from ..hooker import Hooker
from ..internal.modules import Modules

from ..java.helpers.native_method import native_method
from ..utils import memory_helpers,misc_utils

logger = logging.getLogger(__name__)


class NativeHooks:

    def __init__(self, emu, memory, modules, hooker, vfs_root):
        self._emu = emu
        self._memory = memory
        self._modules = modules
        self.__vfs_root = vfs_root
        self.atexit = []

        modules.add_symbol_hook('__system_property_get', hooker.write_function(self.system_property_get) + 1)
        modules.add_symbol_hook('dlopen', hooker.write_function(self.dlopen) + 1)
        modules.add_symbol_hook('dlclose', hooker.write_function(self.dlclose) + 1)
        modules.add_symbol_hook('dladdr', hooker.write_function(self.dladdr) + 1)
        modules.add_symbol_hook('dlsym', hooker.write_function(self.dlsym) + 1)
        modules.add_symbol_hook('dl_unwind_find_exidx', hooker.write_function(self.dl_unwind_find_exidx) + 1)
        modules.add_symbol_hook('pthread_create', hooker.write_function(self.pthread_create) + 1)
        modules.add_symbol_hook('pthread_join', hooker.write_function(self.pthread_join) + 1)

        modules.add_symbol_hook('abort', hooker.write_function(self.abort) + 1)
        modules.add_symbol_hook('dlerror', hooker.write_function(self.nop('dlerror')) + 1)

    @native_method
    def system_property_get(self, uc, name_ptr, buf_ptr):
        name = memory_helpers.read_utf8(uc, name_ptr)
        logger.debug("Called __system_property_get(%s, 0x%x)" % (name, buf_ptr))

        if name in self._emu.system_properties:
            p = self._emu.system_properties[name]
            nread = len(p)
            memory_helpers.write_utf8(uc, buf_ptr, p)
            return nread
        else:
            print ('%s was not found in system_properties dictionary.' % name)
        #
        return 0

    @native_method
    def dlopen(self, uc, path_str):
        path = memory_helpers.read_utf8(uc, path_str)
        logger.debug("Called dlopen(%s)" % path)

        r = 0 
        if (path.find("/") < 0):
            #FIXME:重新考虑谁做vfs路径到android路径的转换关系
            #如果是libxxx.so这种字符串，则直接从
            for mod in self._modules.modules:
                if (mod.filename.find(path)>-1):
                    r = mod.soinfo_ptr
                    logger.debug("Called dlopen(%s) return 0x%08x" %(path, r))
                    return r
                #
            #
        #
        #redirect path on matter what path in vm runing
        fullpath = misc_utils.vfs_path_to_system_path(self.__vfs_root, path)
        if (os.path.exists(fullpath)):
            mod = self._emu.load_library(fullpath)
            r = mod.soinfo_ptr
        else:
            #raise RuntimeError("dlopen %s not found!!!"%fullpath)
            r = 0
        #
        logger.debug("Called dlopen(%s) return 0x%08x" %(path, r))
        return r
    #


    @native_method
    def dlclose(self, uc, handle):
        """
        The function dlclose() decrements the reference count on the dynamic library handle handle.
        If the reference count drops to zero and no other loaded libraries use symbols in it, then the dynamic library is unloaded.
        """
        logger.debug("Called dlclose(0x%x)" % handle)
        return 0
    #

    @native_method
    def dladdr(self, uc, addr, info):
        logger.debug("Called dladdr(0x%x, 0x%x)" % (addr, info))

        infos = memory_helpers.read_uints(uc, info, 4)
        Dl_info = {}

        for mod in self._modules.modules:
            if mod.base <= addr < mod.base + mod.size:
                dli_fname = self._emu.memory.map(0, len(mod.filename) + 1, uc.UC_PROT_READ | uc.UC_PROT_WRITE)
                memory_helpers.write_utf8(uc, dli_fname, mod.filename + '\x00')
                memory_helpers.write_uints(uc, addr, [dli_fname, mod.base, 0, 0])
                return 1
            #
        #
        return 0
    #

    @native_method
    def dlsym(self, uc, handle, symbol):
        symbol_str = memory_helpers.read_utf8(uc, symbol)
        logger.debug("Called dlsym(0x%x, %s)" % (handle, symbol_str))

        if handle == 0xffffffff:
            sym = self._modules.find_symbol_str(symbol_str)
        else:
            soinfo = handle
            #soinfo+140 offset of load base in soinfo on android 4.4
            base = memory_helpers.read_ptr(uc, soinfo+140)

            module = self._modules.find_module(base)

            if module is None:
                raise Exception('Module not found for address 0x%x' % symbol)
            #
            sym = module.find_symbol(symbol_str)
        #
        r = 0
        if sym is not None:
            r = sym
        #
        logger.debug("Called dlsym(0x%x, %s) return 0x%08X" % (handle, symbol_str, r))
        return r
    #

    @native_method
    def abort(self, uc):
        raise RuntimeError("abort called!!!")
        sys.exit(-1)
    #

    @native_method
    def dl_unwind_find_exidx(self, uc, pc, pcount_ptr):
        return 0
    #

    @native_method
    def pthread_create(self, uc, pthread_t, attr, start_routine, arg):
        logging.warning("pthread_create called start_routine [0x%08X]"%(start_routine,))
        return 0
    #

    @native_method
    def pthread_join(self, uc, pthread_t, retval):
        return 0
    #

    def nop(self, name):
        @native_method
        def nop_inside(emu):
            raise NotImplementedError('Symbol hook not implemented %s' % name)
        return nop_inside
    #
