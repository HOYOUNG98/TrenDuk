function displayData() {
    var button = document.getElementById("data");
    
    button.style.display = button.style.display === 'none' ? 'block' : 'none'; 
}



function fetchMove() {
    var pyshell =  require('python-shell');
    pyshell.run('hello.py', function (_, results) {
        document.getElementById("data").innerHTML = "<pre>" + JSON.stringify(JSON.parse(results[0]), null, 2) + "</pre>";

    })
}