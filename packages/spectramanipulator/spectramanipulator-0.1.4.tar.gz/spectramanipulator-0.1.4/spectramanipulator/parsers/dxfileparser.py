import numpy as np
from spectramanipulator.spectrum import Spectrum
from spectramanipulator.parsers.parser import Parser


class DXFileParser(Parser):

    def __init__(self, filepath=None, str_data=None, delimiter=' ', decimal_sep='.',
                 dx_import_spectra_name_from_filename=False, dx_if_title_is_empty_use_filename=True):
        super(DXFileParser, self).__init__(filepath, str_data, delimiter, decimal_sep)

        self.dx_import_spectra_name_from_filename = dx_import_spectra_name_from_filename
        self.dx_if_title_is_empty_use_filename = dx_if_title_is_empty_use_filename

        self.buffer = []

    def _parse_data(self, data, name):

        if len(data) < 2:
            data.clear()
            return

        sp = Spectrum(np.asarray(data, dtype=np.float64), filepath=self.filepath, name=name)
        self.buffer.append(sp)
        data.clear()

    def parse(self, name=''):

        it = self.__iter__()  # get line iterator

        data = []

        # read first header title line
        title_header = it.__next__().strip()
        if name == '':
            try:
                split = title_header.split('=')
                name = split[1][1:]
            except:
                pass

        # if the title field in the dx file is empty, or some error occurred while reading it,
        # use user defined settings

        if self.dx_import_spectra_name_from_filename and not self.dx_if_title_is_empty_use_filename:
            name = self.name_of_file

        if self.dx_if_title_is_empty_use_filename:
            name = self.name_of_file if name == '' else name

        # skip 17 lines of header
        # for i in range(17):
        #     it.__next__()

        # test_split = it.__next__().strip()
        # if self.float_try_parse(test_split[0]) is None:
        #     for i in range(6):
        #         it.__next__()

        # count = 0

        # read the data itself
        for line in it:
            split = line.split(self.delimiter if self.delimiter != '' else None)
            if len(split) < 2:
                self._parse_data(data, name)
                continue

            wavelength = self.float_try_parse(split[0])
            absorbance = self.float_try_parse(split[1])
            if wavelength is None or absorbance is None:
                self._parse_data(data, name)
                continue

            data.append((wavelength, absorbance))

        self._parse_data(data, name)

        # one row will be skipped every time - it is the end line of DX file
        # if count > 1:
        #     Logger.console_message("Warning, {} rows were skipped due to unsuccessful "
        #                            "float value parsing of DX file. Some data may be lost.\nFile: {}".format(count - 1, self.filepath))

        # sp = Spectrum(np.asarray(data, dtype=np.float64), self.filepath, name)
        # return [sp]  # returns a list

        return self.buffer
