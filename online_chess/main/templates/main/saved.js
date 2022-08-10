const chess_room_name = JSON.parse(document.getElementById('chess-room-name').textContent)
    const url = 'ws://' + window.location.host + '/ws/chess_room/' + chess_room_name + '/'
    const chess_room_socket = new WebSocket(url)

    chess_room_socket.onmessage = function(event){
        const data = JSON.parse(event.data).message
        console.log(`[RECEIVING MESSAGE:] ${data}`)
    }

    const form = document.getElementById('form')
    form.addEventListener('submit', (event)=>{
        event.preventDefault()
        var message = event.target.text.value
        console.log(`[SENDING MESSAGE:] ${message}`)
        chess_room_socket.send(JSON.stringify({
            'message': message
        }))

        form.reset()
    })



    <p>This is a chess room{{chess_room_name}}</p>

    <form id='form'>
        <input type='text' name='text'/>
    </form>

    {{chess_room_name|json_script:'chess-room-name'}}