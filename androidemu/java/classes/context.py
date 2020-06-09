from..java_class_def import JavaClassDef
from..java_field_def import JavaFieldDef
from..java_method_def import java_method_def,JavaMethodDef
from .package_manager import *
from .contentresolver import ContentResolver
from .string import String
from .file import File
from ... import config

class Context(metaclass=JavaClassDef, jvm_name='android/content/Context',
                 jvm_fields=[
                     JavaFieldDef('WIFI_SERVICE', 'Ljava/lang/String;', True, "wifi")
                 ]):
    def __init__(self):
        pass
    #

    @java_method_def(name='getPackageManager', signature='()Landroid/content/pm/PackageManager;', native=False)
    def getPackageManager(self, emu):
        raise NotImplementedError()
        pass
    #

    @java_method_def(name='getContentResolver', signature='()Landroid/content/ContentResolver;', native=False)
    def getContentResolver(self, emu):
        raise NotImplementedError()
        pass
    #

    @java_method_def(name='getSystemService', signature='(Ljava/lang/String;)Ljava/lang/Object;', native=False)
    def getSystemService(self, emu, s1):
        raise NotImplementedError()
        pass
    #

    @java_method_def(name='getApplicationInfo', signature='()Landroid/content/pm/ApplicationInfo;', native=False)
    def getApplicationInfo(self, emu):
        raise NotImplementedError()
        pass
    #

    @java_method_def(name='checkSelfPermission', signature='(Ljava/lang/String;)I', native=False)
    def checkSelfPermission(self, emu):
        raise NotImplementedError()
        pass
    #

    @java_method_def(name='checkCallingOrSelfPermission', signature='(Ljava/lang/String;)I', native=False)
    def checkCallingOrSelfPermission(self, emu):
        raise NotImplementedError()
        pass
    #

    @java_method_def(name='getPackageCodePath', signature='()Ljava/lang/String;', native=False)
    def getPackageCodePath(self, emu):
        raise NotImplementedError()
        pass
    #

    @java_method_def(name='getFilesDir', signature='()Ljava/io/File;', native=False)
    def getFilesDir(self, emu):
        raise NotImplementedError()
        pass
    #
#

class ContextImpl(Context, metaclass=JavaClassDef, jvm_name='android/app/ContextImpl', jvm_super=Context):
    def __init__(self):
        Context.__init__(self)

        pyPkgName = config.global_config_get("pkg_name")
        self.__pkgName = String(pyPkgName)
        self.__pkg_mgr = PackageManager(pyPkgName)
        self.__resolver = ContentResolver()
    #
    
    @java_method_def(name='getPackageManager', signature='()Landroid/content/pm/PackageManager;', native=False)
    def getPackageManager(self, emu):
        return self.__pkg_mgr
    #

    @java_method_def(name='getContentResolver', signature='()Landroid/content/ContentResolver;', native=False)
    def getContentResolver(self, emu):
        return self.__resolver
    #

    @java_method_def(name='getSystemService', signature='(Ljava/lang/String;)Ljava/lang/Object;', native=False)
    def getSystemService(self, emu, s1):
        print(s1)
        raise NotImplementedError()
    #

    @java_method_def(name='getApplicationInfo', signature='()Landroid/content/pm/ApplicationInfo;', native=False)
    def getApplicationInfo(self, emu):
        pkgMgr = self.__pkg_mgr
        pkgInfo = pkgMgr.getPackageInfo(emu)
        return pkgInfo.applicationInfo
    #

    @java_method_def(name='getPackageName', signature='()Ljava/lang/String;', native=False)
    def getPackageName(self, emu):
        return self.__pkgName
    #

    @java_method_def(name='checkSelfPermission', signature='(Ljava/lang/String;)I', native=False)
    def checkSelfPermission(self, emu):
        return 0 #PERMISSION_GRANTED
    #

    @java_method_def(name='checkCallingOrSelfPermission', signature='(Ljava/lang/String;)I', native=False)
    def checkCallingOrSelfPermission(self, emu):
        return 0 #PERMISSION_GRANTED
    #

    @java_method_def(name='getPackageCodePath', signature='()Ljava/lang/String;', native=False)
    def getPackageCodePath(self, emu):
        pkgName = config.global_config_get("pkg_name")
        path = "/data/app/%s-1.apk"%(pkgName, )
        return String(path)
    #

    @java_method_def(name='getFilesDir', signature='()Ljava/io/File;', native=False)
    def getFilesDir(self, emu):
        pkgName = config.global_config_get("pkg_name")
        fdir = "/data/data/%s/files"%(pkgName, )
        return File(fdir)
    #
#

class ContextWrapper(Context, metaclass=JavaClassDef, jvm_name='android/content/ContextWrapper', jvm_super=Context):
    
    def __init__(self):
        Context.__init__(self)
        self.__impl = None
    #

    def attachBaseContext(self, ctx_impl):
        self.__impl = ctx_impl
    #

    @java_method_def(name='getPackageManager', signature='()Landroid/content/pm/PackageManager;', native=False)
    def getPackageManager(self, emu):
        return self.__impl.getPackageManager(emu)
    #

    @java_method_def(name='getContentResolver', signature='()Landroid/content/ContentResolver;', native=False)
    def getContentResolver(self, emu):
        return self.__impl.getContentResolver(emu)
    #

    @java_method_def(name='getSystemService', signature='(Ljava/lang/String;)Ljava/lang/Object;', native=False)
    def getSystemService(self, emu, s1):
        return self.__impl.getSystemService(emu, s1)
    #

    @java_method_def(name='getApplicationInfo', signature='()Landroid/content/pm/ApplicationInfo;', native=False)
    def getApplicationInfo(self, emu):
        return self.__impl.getApplicationInfo(emu)
    #

    @java_method_def(name='getPackageName', signature='()Ljava/lang/String;', native=False)
    def getPackageName(self, emu):
        return self.__impl.getPackageName(emu)
    #

    @java_method_def(name='checkSelfPermission', signature='(Ljava/lang/String;)I', native=False)
    def checkSelfPermission(self, emu):
        return self.__impl.checkSelfPermission(emu)
    #

    @java_method_def(name='checkCallingOrSelfPermission', signature='(Ljava/lang/String;)I', native=False)
    def checkCallingOrSelfPermission(self, emu):
        return self.__impl.checkCallingOrSelfPermission(emu)
    #

    @java_method_def(name='getPackageCodePath', signature='()Ljava/lang/String;', native=False)
    def getPackageCodePath(self, emu):
        return self.__impl.getPackageCodePath(emu)
    #

    @java_method_def(name='getFilesDir', signature='()Ljava/io/File;', native=False)
    def getFilesDir(self, emu):
        return self.__impl.getFilesDir(emu)
    #
#