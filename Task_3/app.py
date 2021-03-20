from flask import Flask, request, jsonify, abort
from utils import appearance

app = Flask(__name__)


@app.route('/appearance', methods=['GET', 'POST'])
def returned_joint_time_presence():
    if request.method == 'GET':
        return jsonify({
            'text': 'Для получения общего времени присутсвия преподавателя и ученика на уроке, отправьте мне интервалы их присутствия.'})

    if request.method == 'POST':
        if not request.json:
            abort(400)

        intervals = {
            'lesson': request.json['lesson'],
            'pupil': request.json['pupil'],
            'tutor': request.json['tutor'],
        }
        response = appearance(intervals)
        return jsonify({'time_joint_presence': response})


if __name__ == '__main__':
    app.run(debug=True)
