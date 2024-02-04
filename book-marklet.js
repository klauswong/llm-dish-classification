// Expanded version for readability
startTime = new Date().getTime()
fetch('http://localhost:8000/classify_dishes', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    'body': JSON.stringify(
        Array.from(
            document.querySelectorAll("span[data-testid='menu-product-name']"))
            .map(x => x.innerText))
})
    .then(res => res.json())
    .then(d => alert("Used: " + (new Date().getTime() - startTime) / 1000 + "secs\n" + d.map(item => item.dish_name).join("\n")))

// The one-liner version
// javascript: startTime = new Date().getTime();fetch('http://localhost:8000/classify_dishes', { method: 'POST', headers: { 'Content-Type': 'application/json' }, 'body': JSON.stringify(Array.from(document.querySelectorAll("span[data-testid='menu-product-name']")).map(x => x.innerText)) }).then(res => res.json()).then(d => alert("Used: " + (new Date().getTime() - startTime) / 1000 + "secs\n" + d.map(item => item.dish_name).join("\n")))