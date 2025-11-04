document.getElementById('helloBtn').addEventListener('click', async () => {
    const res = await fetch('https://flask-api-gateway-6jq682pn.ew.gateway.dev/hello');
    const data = await res.json();
    document.getElementById('response').innerText = data.message;
});
