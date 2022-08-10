const chess_room_form = document.getElementById('chess_room_form')
    chess_room_form.addEventListener('submit', (event)=>{
        event.preventDefault() // this is very important and prevents broken pipes (whatever the fuck that means)
        let message = event.target.chess_room_input.value
        // send this to the server (or, reroute from js)
        console.log(message)
        window.location.pathname = '/game/' + message + '/'
    })