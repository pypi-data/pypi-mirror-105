import pickle
from spectramanipulator.settings import Settings
from spectramanipulator.logger import Logger
import spectramanipulator
import sys

COMPRESS_LEVEL = 3

# used for backward compatibility
class SafeUnpickler(pickle.Unpickler):
    # help from https://www.programcreek.com/python/example/1606/pickle.Unpickler
    # https://stackoverflow.com/questions/13398462/unpickling-python-objects-with-a-changed-module-path

    def find_class(self, module, name):
        """
        Overridden from the original 'Unpickler' class. Needed to rebuild PyMod object which have
        complex modules names. 'Unpickler' rebuilds objects using the 'fully qualified' name
        reference of their classes (the class name is pickled, along with the name of the module the
        class is defined in). Since PyMOL plugin modules may yield different 'fully qualified' names
        depending on the system, PyMod objects are rebuilt using only the name of their classes.
        """

        if name == 'SpectrumList':  # for very old backward compatibility
            return list

        # Try the standard routine of pickle.
        try:
            # print(module)
            __import__(module)
        except ImportError:  # for backward compatibility when the program was not a python Package
            print(f'import of {module} failed, adding spectramanipulator.')
            module = f'spectramanipulator.{module}'
            __import__(module)

        mod = sys.modules[module]
        klass = getattr(mod, name)
        return klass


class Project:

    def __init__(self, generic_item=None, *args):

        # self.spectra_list = spectra_list  # used in older program versions
        self.generic_item = generic_item
        self.settings = Settings()  # saves the static attributes to instance attributes that are saved

        self.args = args
        self.__version__ = spectramanipulator.__version__

    def serialize(self, filepath):
        try:
            with open(filepath, 'bw') as file:
                pickle.dump(self, file)

            # try:
            # except:
            #     pass

            # with bz2.BZ2File(filepath, 'w', compresslevel=COMPRESS_LEVEL) as file:
            #     pickle.dump(self, file)

        # except pickle.PicklingError as err:
        #     Logger.console_message("Unable to save current project:\n{}\n{}".format(err.__str__(), err.__traceback__))
        #     raise Exception
        except Exception as err:
            Logger.message("Unable to save current project:\n{}".format(err.__str__()))
            raise

    @staticmethod
    def deserialize(filepath):

        # instance = pickle.load(open(filepath, 'rb'))

        instance = SafeUnpickler(open(filepath, 'rb')).load()
        return instance

        # try:
        #     try:
        #         # with open(filepath, 'br') as file:
        #         #     instance = pickle.load(file)
        #         instance = SafeUnpickler(open(filepath, 'rb')).load()
        #     except:  # for maintaining compatibility
        #         import bz2
        #         with bz2.BZ2File(filepath, 'r', compresslevel=COMPRESS_LEVEL) as file:
        #             instance = pickle.load(file)
        #
        #     return instance
        # # except pickle.UnpicklingError as err:
        # #     Logger.send_message("Unable to load {}:\n{}\n{}".format(filepath, err.__str__(), err.__traceback__))
        # #     raise
        # except Exception as err:
        #     Logger.message("Unable to load {}.\n{}".format(filepath, err.__str__()))






