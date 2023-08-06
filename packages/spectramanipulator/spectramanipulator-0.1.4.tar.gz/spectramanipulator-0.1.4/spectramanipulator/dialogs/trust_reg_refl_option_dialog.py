from PyQt5 import QtWidgets

from PyQt5.QtWidgets import QLineEdit, QComboBox
from spectramanipulator.dialogs.genericinputdialog import GenericInputDialog

from webbrowser import open_new_tab


class TrustRegionReflOptionDialog(GenericInputDialog):

    def __init__(self, ftol=1e-8, xtol=1e-8, gtol=1e-8, loss: str = 'linear',
                 max_nfev=None, verbose: int = 2, set_result=None):

        if self.is_opened:
            return

        # https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.least_squares.html

        self.options = self.default_opts()

        self.options.update(ftol=ftol, xtol=xtol, gtol=gtol, loss=loss,
                            max_nfev=max_nfev, verbose=verbose)

        widget_list = []

        self.ftol_edit = QLineEdit(str(ftol))
        self.xtol_edit = QLineEdit(str(xtol))
        self.gtol_edit = QLineEdit(str(gtol))

        # self.minim_alg_opts = [
        #     {'opt': 'trf', 'description': 'Trust Region Reflective algorithm, particularly suitable for large sparse problems with bounds. Generally robust method.'},
        #     {'opt': 'dogbox', 'description': 'Dogleg algorithm with rectangular trust regions, typical use case is small problems with bounds. Not recommended for problems with rank-deficient Jacobian.'},
        #     {'opt': 'lm', 'description': 'Levenberg-Marquardt algorithm as implemented in MINPACK. Doesn’t handle bounds and sparse Jacobians. Usually the most efficient method for small unconstrained problems.'},
        # ]

        self.loss_options = [
            {'opt': 'linear', 'description': 'rho(z) = z. Gives a standard least-squares problem.'},
            {'opt': 'soft_l1', 'description': 'rho(z) = 2 * ((1 + z)**0.5 - 1). The smooth approximation of l1 (absolute value) loss. Usually a good choice for robust least squares.'},
            {'opt': 'huber', 'description': 'rho(z) = z if z <= 1 else 2*z**0.5 - 1. Works similarly to ‘soft_l1’.'},
            {'opt': 'cauchy', 'description': 'rho(z) = ln(1 + z). Severely weakens outliers influence, but may cause difficulties in optimization process.'},
            {'opt': 'arctan', 'description': 'rho(z) = arctan(z). Limits a maximum loss on a single residual, has properties similar to ‘cauchy’.'},
        ]

        self.verbose_opts = [
            {'opt': 0, 'description': 'Works silently'},
            {'opt': 1, 'description': 'Displays a termination report.'},
            {'opt': 2, 'description': 'Displays progress during iterations (not supported by ‘lm’ method)'},
        ]

        # self.alg_cb = QComboBox()
        # self.alg_cb.addItems(map(lambda o: o['description'], self.minim_alg_opts))
        # _opts = list(map(lambda o: o['opt'], self.minim_alg_opts))
        # self.alg_cb.setCurrentIndex(_opts.index(method))

        self.loss_cb = QComboBox()
        self.loss_cb.addItems(map(lambda o: f"{o['opt']}: {o['description']}", self.loss_options))
        _opts = list(map(lambda o: o['opt'], self.loss_options))
        self.loss_cb.setCurrentIndex(_opts.index(loss))

        self.max_nfev_edit = QLineEdit(str(max_nfev))

        self.verbose_cb = QComboBox()
        self.verbose_cb.addItems(map(lambda o: f"{o['opt']}: {o['description']}", self.verbose_opts))
        _opts = list(map(lambda o: o['opt'], self.verbose_opts))
        self.verbose_cb.setCurrentIndex(_opts.index(verbose))

        # widget_list.append(('Algorithm to perform minimization:', self.alg_cb))
        widget_list.append(('ftol:', self.ftol_edit))
        widget_list.append(('xtol:', self.xtol_edit))
        widget_list.append(('gtol:', self.gtol_edit))
        widget_list.append(('Loss function:', self.loss_cb))
        widget_list.append(('Max n_fev:', self.max_nfev_edit))
        widget_list.append(('Verbose:', self.verbose_cb))

        description = """<html><head/><body><p>For explanation, see 
        <a href="https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.least_squares.html">
        <span style=" text-decoration: underline; color:#0000ff;">scipy.optimize.least_squares</span></a>.</p></body></html>"""

        super(TrustRegionReflOptionDialog, self).__init__(widget_list=widget_list,
                                                          label_text=description,
                                                          title='Settings of Trust Region Reflective algorithm',
                                                          parent=None,
                                                          set_result=set_result)

        self.label.linkActivated.connect(lambda: open_new_tab("https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.least_squares.html"))


    @staticmethod
    def default_opts():
        return dict(ftol=1e-8, xtol=1e-8, gtol=1e-8, loss='linear',
                    max_nfev=None, verbose=2)

    def accept(self):
        # self.options['method'] = self.minim_alg_opts[self.alg_cb.currentIndex()]['opt']
        self.options['loss'] = self.loss_options[self.loss_cb.currentIndex()]['opt']
        self.options['verbose'] = self.verbose_opts[self.verbose_cb.currentIndex()]['opt']
        try:
            self.options['ftol'] = float(self.ftol_edit.text())
        except ValueError:
            self.options['ftol'] = None
        try:
            self.options['xtol'] = float(self.xtol_edit.text())
        except ValueError:
            self.options['xtol'] = None
        try:
            self.options['gtol'] = float(self.gtol_edit.text())
        except ValueError:
            self.options['gtol'] = None
        try:
            self.options['max_nfev'] = float(self.max_nfev_edit.text())
        except ValueError:
            self.options['max_nfev'] = None

        super(TrustRegionReflOptionDialog, self).accept()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = TrustRegionReflOptionDialog()
    Dialog.show()
    sys.exit(app.exec_())

