import sys
import terver
import PyQt5.QtWidgets
import json
import pandas
from exception import ParametersError
import Exponential
import Poisson
import Binomial
import openpyxl
import glob

def ExcelWrite(name, lst, description):
    try:
        excel_file=pandas.ExcelFile("Distributions.xlsx", engine='openpyxl')
        sheet_names=excel_file.sheet_names
    except FileNotFoundError:
        sheet_names=[]
    dict={}
    if len(sheet_names)!=0:
        for sheet_name in sheet_names:
            df=pandas.read_excel("./Distributions.xlsx",sheet_name=sheet_name)
            part_dict={}
            for i in df:
                print(i)
                if i=="Unnamed: 0":
                    continue
                part_dict.update({i: df[i].tolist()})
            dict.update({sheet_name:part_dict})
    print(len(dict))
    if name in dict.keys():
        if len(dict[name])!=0:
            if len(dict[name][1])>len(lst)+1:
                for i in range(len(dict[name][1])-len(lst)-1):
                    lst.append("-")
            elif len(dict[name][1])<len(lst)+1:
                for i in range(1,len(dict[name])+1):
                    for j in range(len(lst)-len(dict[name][i])+1):
                        dict[name][i].append("-")
        dict[name].update({len(dict[name])+1:[description]+lst})
    else:
        dict.update({name:{1:[description]+lst}})
    print(dict)
    with pandas.ExcelWriter("./Distributions.xlsx") as writer:
        for names in dict.keys():
            if len(dict[names])==0:
                continue
            new_df=pandas.DataFrame(dict[names])
            new_df.to_excel(writer, sheet_name=names, index=False)

class MainWindow(PyQt5.QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Главное окно")
        self.setGeometry(300, 100, 300, 200)

        self.label = PyQt5.QtWidgets.QLabel(self)
        self.label.setText("Название распределения:")
        self.label.move(20, 20)

        self.combobox = PyQt5.QtWidgets.QComboBox(self)
        self.combobox.addItem("Равномерное")
        self.combobox.addItem("Нормальное")
        self.combobox.addItem("Логнормальное")
        self.combobox.addItem("Пуассона")
        self.combobox.addItem("Экспоненциальное")
        self.combobox.addItem("Биномиальное")
        self.combobox.move(20, 50)

        self.button = PyQt5.QtWidgets.QPushButton(self)
        self.button.setText("Отправить")
        self.button.move(20, 80)
        self.button.clicked.connect(self.openSecondWindow)

        self.buttonReset = PyQt5.QtWidgets.QPushButton(self)
        self.buttonReset.setText("Очистить таблицу")
        self.buttonReset.move(120, 80)
        self.buttonReset.clicked.connect(self.resetDistributions)

    def resetDistributions(self):
        new_df=pandas.DataFrame({})
        new_df.to_excel("./Distributions.xlsx")

    def openSecondWindow(self):
        distribution_name = self.combobox.currentText()

        if distribution_name == "Равномерное":
            self.uniform_window = UniformDistributionWindow()
            self.uniform_window.show()
        elif distribution_name == "Нормальное":
            self.normal_window = NormalDistributionWindow()
            self.normal_window.show()
        elif distribution_name == "Логнормальное":
            self.normal_window = LogNormalDistributionWindow()
            self.normal_window.show()
        elif distribution_name == "Пуассона":
            self.poisson_window = PoissonDistributionWindow()
            self.poisson_window.show()
        elif distribution_name == "Экспоненциальное":
            self.exponential_window=ExponentialDistributionWindow()
            self.exponential_window.show()
        elif distribution_name=="Биномиальное":
            self.binomial_window=BinomialDistributionWindow()
            self.binomial_window.show()

        


class UniformDistributionWindow(PyQt5.QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Окно с равномерным распределением")
        self.setGeometry(100, 100, 500, 200)

        self.label1 = PyQt5.QtWidgets.QLabel(self)
        self.label1.setText("Количество чисел:")
        self.label1.move(20, 20)

        self.textbox1 = PyQt5.QtWidgets.QLineEdit(self)
        self.textbox1.move(20, 50)

        self.label2 = PyQt5.QtWidgets.QLabel(self)
        self.label2.setText("От:")
        self.label2.move(20, 80)

        self.textbox2 = PyQt5.QtWidgets.QLineEdit(self)
        self.textbox2.move(40, 80)

        self.label3 = PyQt5.QtWidgets.QLabel(self)
        self.label3.setText("До:")
        self.label3.move(20, 110)

        self.textbox3 = PyQt5.QtWidgets.QLineEdit(self)
        self.textbox3.move(40,110)

        self.button = PyQt5.QtWidgets.QPushButton(self)
        self.button.setText("Отправить")
        self.button.move(20, 140)
        self.button.clicked.connect(self.getData)

    def getData(self):
        number_count = self.textbox1.text()
        begin = self.textbox2.text()
        end=self.textbox3.text()
        number_count = int(number_count)
        if not begin or not end:
            PyQt5.QtWidgets.QMessageBox.warning(self, "Вы не ввели диапазон", "Попробуйте ещё раз")
            self.textbox2.clear()
        else:
            try:
                begin = float(begin)
                end = float(end)
            except Exception:
                PyQt5.QtWidgets.QMessageBox.warning(self, "Неверно введены данные(должно соответствовать шаблону)",
                                    "Попробуйте ещё раз")
                self.textbox4.clear()

            if number_count < 0:
                PyQt5.QtWidgets.QMessageBox.warning(self, "Количество чисел должно быть положительным", "Попробуйте ещё раз")
                self.textbox1.clear()
            if begin > end:
                PyQt5.QtWidgets.QMessageBox.warning(self, "Отрицательный диапазон", "Попробуйте ещё раз")
                self.textbox2.clear()
            else:
                lst = terver.conversation_uniform(int(number_count), f"from {begin} to {end}")
                info_tuple = ['from', str(begin), 'to', str(end)]

                ExcelWrite("равномерное", lst, f"{begin=}, {end=}")
                with open("config.json", 'a', encoding="utf-8") as file:
                    json.dump("uniform", file)
                    file.write('\n')
                    json.dump(info_tuple, file)
                    file.write('\n')
                    json.dump(lst, file)
                    file.write('\n')
                    file.write('\n')



class NormalDistributionWindow(PyQt5.QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Окно с нормальным распределением")
        self.setGeometry(300, 100, 500, 400)

        self.label1 = PyQt5.QtWidgets.QLabel(self)
        self.label1.setText("Математическое ожидание:")
        self.label1.move(20, 20)

        self.textbox1 = PyQt5.QtWidgets.QLineEdit(self)
        self.textbox1.move(20, 50)

        self.label2 = PyQt5.QtWidgets.QLabel(self)
        self.label2.setText("Среднеквадратическое отклонение:")
        self.label2.move(20, 80)

        self.textbox2 = PyQt5.QtWidgets.QLineEdit(self)
        self.textbox2.move(20, 110)

        self.label3 = PyQt5.QtWidgets.QLabel(self)
        self.label3.setText("Количество чисел:")
        self.label3.move(20, 140)

        self.textbox3 = PyQt5.QtWidgets.QLineEdit(self)
        self.textbox3.move(20, 170)

        self.label4 = PyQt5.QtWidgets.QLabel(self)
        self.label4.setText("От:")
        self.label4.move(20, 200)

        self.textbox4 = PyQt5.QtWidgets.QLineEdit(self)
        self.textbox4.move(40, 200)

        self.label5 = PyQt5.QtWidgets.QLabel(self)
        self.label5.setText("До:")
        self.label5.move(20, 230)

        self.textbox5 = PyQt5.QtWidgets.QLineEdit(self)
        self.textbox5.move(40,230)

        self.button = PyQt5.QtWidgets.QPushButton(self)
        self.button.setText("Отправить")
        self.button.move(20, 260)
        self.button.clicked.connect(self.getData)

    def getData(self):
        math_wait = self.textbox1.text()

        derivation = self.textbox2.text()
        quantity = self.textbox3.text()
        begin = self.textbox4.text()
        end = self.textbox5.text()
        try:
            begin = float(begin)
            end = float(end)
        except Exception:
            PyQt5.QtWidgets.QMessageBox.warning(self, "Неверно введены данные(должно соответствовать шаблону)",
                                "Попробуйте ещё раз")
            self.textbox4.clear()
        try:
            math_wait = float(math_wait)
        except ValueError:
            PyQt5.QtWidgets.QMessageBox.warning(self, "Математическое ожидание должно быть вещественным числом", "Попробуйте ещё раз")
            self.textbox1.clear()
        try:
            derivation = float(derivation)
        except ValueError:
            PyQt5.QtWidgets.QMessageBox.warning(self, " Среднеквадратическое отклонение должно быть вещественным числом",
                                "Попробуйте ещё раз")
            self.textbox2.clear()
        else:
            quantity = int(quantity)
            try:
                if quantity < 0:
                    raise AttributeError
                if begin > end:
                    raise ArithmeticError
                if math_wait < begin or math_wait > end:
                    raise BaseException
            except AttributeError:
                PyQt5.QtWidgets.QMessageBox.warning(self, "Количество чисел - положительное число", "Попробуйте ещё раз")
                self.textbox3.clear()
            except ArithmeticError:
                PyQt5.QtWidgets.QMessageBox.warning(self, "Отрицательный диапазон", "Попробуйте ещё раз")
                self.textbox4.clear()
            except BaseException:
                PyQt5.QtWidgets.QMessageBox.warning(self, "Математическое ожидание не входит в диапазон", "Попробуйте ещё раз")
                self.textbox1.clear()
            else:
                lst = terver.conversation_normal(math_wait, derivation, quantity, f"from {begin} to {end}", "normal")
                info_tuple = ['from', str(begin), 'to', str(end)]
                ExcelWrite("нормальное",lst,f'{begin=}, {end=}, {derivation=}, expected value={math_wait}')
                with open("config.json", 'a', encoding="utf-8") as file:
                    json.dump("normal", file)
                    file.write('\n')
                    json.dump(info_tuple, file)
                    file.write('\n')
                    json.dump(lst, file)
                    file.write('\n')
                    file.write('\n')


class LogNormalDistributionWindow(PyQt5.QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Окно с логнормальным распределением")
        self.setGeometry(300, 100, 500, 400)

        self.label1 = PyQt5.QtWidgets.QLabel(self)
        self.label1.setText("Математическое ожидание:")
        self.label1.move(20, 20)

        self.textbox1 = PyQt5.QtWidgets.QLineEdit(self)
        self.textbox1.move(20, 50)

        self.label2 = PyQt5.QtWidgets.QLabel(self)
        self.label2.setText("Среднеквадратическое отклонение:")
        self.label2.move(20, 80)

        self.textbox2 = PyQt5.QtWidgets.QLineEdit(self)
        self.textbox2.move(20, 110)

        self.label3 = PyQt5.QtWidgets.QLabel(self)
        self.label3.setText("Количество чисел:")
        self.label3.move(20, 140)

        self.textbox3 = PyQt5.QtWidgets.QLineEdit(self)
        self.textbox3.move(20, 170)

        self.label4 = PyQt5.QtWidgets.QLabel(self)
        self.label4.setText("От:")
        self.label4.move(20, 200)

        self.textbox4 = PyQt5.QtWidgets.QLineEdit(self)
        self.textbox4.move(40, 200)

        self.label5 = PyQt5.QtWidgets.QLabel(self)
        self.label5.setText("До:")
        self.label5.move(20, 230)

        self.textbox5 = PyQt5.QtWidgets.QLineEdit(self)
        self.textbox5.move(40, 230)

        self.button = PyQt5.QtWidgets.QPushButton(self)
        self.button.setText("Отправить")
        self.button.move(20, 260)
        self.button.clicked.connect(self.getData)

    def getData(self):
        math_wait = self.textbox1.text()
        derivation = self.textbox2.text()
        quantity = self.textbox3.text()

        try:
            math_wait = float(math_wait)
        except ValueError:
            PyQt5.QtWidgets.QMessageBox.warning(self, "Математическое ожидание должно быть вещественным числом", "Попробуйте ещё раз")
            self.textbox1.clear()
        try:
            derivation = float(derivation)
        except ValueError:
            PyQt5.QtWidgets.QMessageBox.warning(self, " Среднеквадратическое отклонение должно быть вещественным числом", "Попробуйте ещё раз")
            self.textbox2.clear()

        else:
            quantity = int(quantity)
            begin=self.textbox4.text()
            end=self.textbox5.text()
            try:
                begin = float(begin)
                end = float(end)
            except Exception:
                PyQt5.QtWidgets.QMessageBox.warning(self, "Неверно введены данные(должно соответствовать шаблону)",
                                    "Попробуйте ещё раз")
                self.textbox4.clear()
            try:
                if begin < 0:
                    raise ValueError
                if quantity < 0:
                    raise AttributeError
                if begin > end:
                    raise ArithmeticError
                if math_wait < begin or math_wait > end:
                    raise BaseException


            except ValueError:
                PyQt5.QtWidgets.QMessageBox.warning(self, " Логнормальное распределение не может включать отрицательных чисел",
                                    "Введите диапазон, включающий в себя только неотрицательные числа")
                self.textbox4.clear()

            except AttributeError:
                PyQt5.QtWidgets.QMessageBox.warning(self, "Количество чисел - положительное число", "Попробуйте ещё раз")
                self.textbox3.clear()
            except ArithmeticError:
                PyQt5.QtWidgets.QMessageBox.warning(self, "Отрицательный диапазон", "Попробуйте ещё раз")
                self.textbox4.clear()
            except BaseException:
                PyQt5.QtWidgets.QMessageBox.warning(self, "Математическое ожидание не входит в диапазон", "Попробуйте ещё раз")
                self.textbox1.clear()
            else:
                lst = terver.conversation_normal(math_wait, derivation, quantity, f"from {begin} to {end}", "lognormal")

                info_tuple = ['from', str(begin), 'to', str(end)]
                ExcelWrite("логнормальное",lst,f"{begin=}, {end=}, {derivation=}, expected value={math_wait}")
                with open("config.json", 'a', encoding="utf-8") as file:
                    json.dump("lognormal", file)
                    file.write('\n')
                    json.dump(info_tuple, file)
                    file.write('\n')
                    json.dump(lst, file)
                    file.write('\n')
                    file.write('\n')



class PoissonDistributionWindow(PyQt5.QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Окно с распределением Пуассона")
        self.setGeometry(300, 100, 500, 300)

        self.label1 = PyQt5.QtWidgets.QLabel(self)
        self.label1.setText("Математическое ожидание:")
        self.label1.move(20, 20)

        self.textbox1 = PyQt5.QtWidgets.QLineEdit(self)
        self.textbox1.move(20, 50)

        self.label2 = PyQt5.QtWidgets.QLabel(self)
        self.label2.setText("Количество испытаний:")
        self.label2.move(20, 80)

        self.textbox2 = PyQt5.QtWidgets.QLineEdit(self)
        self.textbox2.move(20, 120)

        self.button = PyQt5.QtWidgets.QPushButton(self)
        self.button.setText("Отправить")
        self.button.move(20, 160)
        self.button.clicked.connect(self.getData)

    def getData(self):
        math_wait = self.textbox1.text()
        quantity = self.textbox2.text()

        try:
            math_wait = int(math_wait)
        except ValueError:
            PyQt5.QtWidgets.QMessageBox.warning(self, "Математическое ожидание должно быть вещественным числом", "Попробуйте ещё раз")
            self.textbox1.clear()
        else:
            quantity = int(quantity)
            if quantity < 0:
                PyQt5.QtWidgets.QMessageBox.warning(self, "Количество испытаний - положительное число", "Попробуйте ещё раз")
                self.textbox2.clear()

            else:
                lst = Poisson.Poisson_Generator(math_wait,quantity)
                ExcelWrite("Пуассоновское",lst,f'expected value={math_wait}')
                terver.Draw_Distribution(Poisson.Poisson_Function,math_wait+10,0,{"rate":math_wait},isDiscret=True)
                with open("config.json", 'a', encoding="utf-8") as file:
                    json.dump("poisson", file)
                    file.write('\n')
                    json.dump(lst, file)
                    file.write('\n')
                    file.write('\n')

class ExponentialDistributionWindow(PyQt5.QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Окно с экспоненциальным распределением")
        self.setGeometry(300, 100, 500, 300)

        self.label1 = PyQt5.QtWidgets.QLabel(self)
        self.label1.setText("Интенсивность:")
        self.label1.move(20, 20)

        self.textbox1 = PyQt5.QtWidgets.QLineEdit(self)
        self.textbox1.move(20, 50)

        self.label2 = PyQt5.QtWidgets.QLabel(self)
        self.label2.setText("Количество испытаний:")
        self.label2.move(20, 80)

        self.textbox2 = PyQt5.QtWidgets.QLineEdit(self)
        self.textbox2.move(20, 110)

        self.label3 = PyQt5.QtWidgets.QLabel(self)
        self.label3.setText("До какого значения:")
        self.label3.move(20,140)

        self.textbox3 = PyQt5.QtWidgets.QLineEdit(self)
        self.textbox3.move(20,160)

        self.button = PyQt5.QtWidgets.QPushButton(self)
        self.button.setText("Отправить")
        self.button.move(20, 240)
        self.button.clicked.connect(self.getData)
    
    def getData(self):
        intensity=self.textbox1.text()
        count=self.textbox2.text()
        max=self.textbox3.text()
        status_intensity=False; status_count=False; status_max=False
        try:
            intensity=float(intensity)
            if intensity<0:
                raise ParametersError
        except ValueError:
            PyQt5.QtWidgets.QMessageBox.warning(self,"Интенсивность должна быть числом","Попробуйте еще раз!")
            self.textbox1.clear()
        except ParametersError:
            PyQt5.QtWidgets.QMessageBox.warning(self,"Интенсивность должна быть положительным числом","Попробуйте еще раз!")
            self.textbox1.clear()
        else:
            status_intensity=True
        try:
            count=int(count)
            if count<=0:
                raise ParametersError
        except ValueError:
            PyQt5.QtWidgets.QMessageBox.warning(self,"Количество экспериментов должно быть целым числом","Попробуйте еще раз!")
            self.textbox2.clear()
        except ParametersError:
            PyQt5.QtWidgets.QMessageBox.warning(self,"Количество экспериментов должно быть целым положительным числом","Попробуйте еще раз!")
            self.textbox2.clear()
        else:
            status_count=True
        try:
            max=float(max)
            if max<=0:
                raise ParametersError
        except ValueError:
            PyQt5.QtWidgets.QMessageBox.warning(self,"Максимальное число должно быть числом","Попробуйте еще раз!")
            self.textbox2.clear()
        except ParametersError:
            PyQt5.QtWidgets.QMessageBox.warning(self,"Максимальное число должно быть положительным числом","Попробуйте еще раз!")
            self.textbox2.clear()
        else:
            status_max=True
        if status_intensity and status_count and status_max:
            if max<1/intensity+1/(intensity*intensity):
                PyQt5.QtWidgets.QMessageBox.warning(self,"Внимание","Значения, могут получиться неверными!")
            lst=Exponential.Exponential_Generator(intensity,max,count)
            ExcelWrite("Экспоненциальное",lst,f'{intensity=},{max=}')
            terver.Draw_Distribution(Exponential.Exponential_Density_Function,max,0,{"intensity":intensity})

class BinomialDistributionWindow(PyQt5.QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Окно с биномиальным распределением")
        self.setGeometry(300, 100, 500, 300)

        self.label1 = PyQt5.QtWidgets.QLabel(self)
        self.label1.setText("Вероятность успеха:")
        self.label1.move(20, 20)

        self.textbox1 = PyQt5.QtWidgets.QLineEdit(self)
        self.textbox1.move(20, 50)

        self.label2 = PyQt5.QtWidgets.QLabel(self)
        self.label2.setText("Количество испытаний:")
        self.label2.move(20, 80)

        self.textbox2 = PyQt5.QtWidgets.QLineEdit(self)
        self.textbox2.move(20, 110)

        self.label3 = PyQt5.QtWidgets.QLabel(self)
        self.label3.setText("Количество чисел:")
        self.label3.move(20, 140)

        self.textbox3 = PyQt5.QtWidgets.QLineEdit(self)
        self.textbox3.move(20, 160)

        self.button = PyQt5.QtWidgets.QPushButton(self)
        self.button.setText("Отправить")
        self.button.move(20, 240)
        self.button.clicked.connect(self.getData)
    
    def getData(self):
        probability=self.textbox1.text()
        n=self.textbox2.text()
        count=self.textbox3.text()
        status_probability=False; status_count=False; status_n=False
        try:
            count=int(count)
            if count<=0:
                raise ParametersError("")
        except ValueError:
            PyQt5.QtWidgets.QMessageBox.warning(self,"Количество экспериментов должно быть целым числом","Попробуйте еще раз!")
            self.textbox3.clear()
        except ParametersError:
            PyQt5.QtWidgets.QMessageBox.warning(self,"Количество экспериментов должно быть целым положительным числом","Попробуйте еще раз!")
            self.textbox3.clear()
        else:
            status_count=True
        try:
            n=int(n)
            if n<=0:
                raise ParametersError("")
        except ValueError:
            PyQt5.QtWidgets.QMessageBox.warning(self,"Количество экспериментов должно быть целым числом","Попробуйте еще раз!")
            self.textbox2.clear()
        except ParametersError:
            PyQt5.QtWidgets.QMessageBox.warning(self,"Количество экспериментов должно быть целым положительным числом","Попробуйте еще раз!")
            self.textbox2.clear()
        else:
            status_n=True
        try:
            probability=float(probability)
            if probability<=0 or probability>=1:
                raise ParametersError("")
        except ValueError:
            PyQt5.QtWidgets.QMessageBox.warning(self,"Количество экспериментов должно быть целым числом","Попробуйте еще раз!")
            self.textbox1.clear()
        except ParametersError:
            PyQt5.QtWidgets.QMessageBox.warning(self,"Вероятность должна находиться в интервале (0;1)","Попробуйте еще раз!")
            self.textbox1.clear()
        else:
            status_probability=True
        if status_count and status_probability and status_n:
            lst=Binomial.Binomial_Generator(probability,n,count)
            ExcelWrite("Биномиальное",lst,f'{probability=}, number of trials={n}')
            terver.Draw_Distribution(Binomial.Binomial_Function,n,0,{"n":n,"p":probability},isDiscret=True)



if __name__ == "__main__":
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())