async function sendNumbers() {
    const num1 = parseFloat(document.getElementById('num1').value);
    const num2 = parseFloat(document.getElementById('num2').value);

    const response = await fetch('http://127.0.0.1:5000/sum', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ num1, num2 })
    });

    const data = await response.json();
    document.getElementById('result').textContent = 'Result: ' + data.result;
}
