from flask import Flask,request,render_template,url_for,redirect
from flask_socketio import SocketIO,leave_room,join_room

clients_list={}

app=Flask(__name__)
socketio=SocketIO(app)

@app.route('/')
def homepage():
    return render_template('input1.html')



@app.route('/again_join_url/<username>' ,methods=['GET','POST'])
def again_join_url(username):
    return render_template('again_input.html',username=username)




@socketio.on('join_room')
def handle_join_room(data):

    if clients_list.get(data['room'],0)==0:
        clients_list[data['room']]=[]



    if data['username'] not in clients_list[data['room']]:
        clients_list[data['room']].append(data['username'])
    else:
        socketio.emit('already', {'username':data['username']});


    join_room(data['room'])
    print('join {} '.format(data['username']))
    socketio.emit('room_joined', data, room=data['room'])





@socketio.on('leave_room')
def leave_room_handler(data):
    leave_room(data['room'])
    clients_list[data['room']].remove(data['username'])
    socketio.emit('leaved_room',{'room':data['room'],'username':data['username']})

@socketio.on('show_online')
def show_online(data):
    room_no=data['room']
    str_data='<br>'.join(clients_list[room_no])
    socketio.emit('online_result',{'result':str_data,'username':data['username']},room=data['room']);

@socketio.on('send_message')
def hand_client_message(data):
    socketio.emit('receive_msg',data,room=data['room'])

@app.route('/input',methods=['GET','POST'])
def input():
    username=request.form['username']
    roomid=request.form['roomid']
    if username and roomid:
        return  render_template('chat1.html',username=username,room=roomid)

    else:
        return redirect(url_for('homepage'))





if __name__=="__main__":
    socketio.run(app,debug=True,host='localhost',port=5001);
