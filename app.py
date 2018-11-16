from flask import Flask, request, render_template, redirect, url_for
from json import dumps
from elo import compare, choose,  males, males_list, females, females_list
from threading import Timer
from random import choice

# https://stackoverflow.com/questions/3393612/run-certain-code-every-n-seconds


class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


app = Flask(__name__)


def sort_lists():
    global males, males_list, females, females_list
    males_list = sorted(males, key=males.get)
    females_list = sorted(females, key=females.get)


@app.route('/', methods=["GET", "POST"])
def index():
    gender = choice([True, False])
    names = choose(gender)
    return render_template('index.html', name1=names[0], name2=names[1], gender='f' if gender else 'm', link_to=url_for('female_results') if gender else url_for('male_results'))


@app.route('/choice/<my_choice>/<not_choice>/<gender>/')
def add(my_choice, not_choice, gender):
    is_female = gender is 'f'

    compare(my_choice, not_choice, is_female, 1)
    return redirect(url_for('index'))


@app.route('/results/m')
def male_results():
    global males_list
    return render_template('results.html', names=males_list, gender='Coolest Male Names')


@app.route('/results/f')
def female_results():
    global females_list
    return render_template('results.html', names=females_list, gender='Coolest Female Names')


rt = RepeatedTimer(10, sort_lists)  # it auto-starts, no need of rt.start()
try:
    sort_lists()
    app.run()
finally:
    rt.stop()
