chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "summarize") {
        // Call your backend API or perform local summarization
        fetch("http://127.0.0.1:8000/gettext/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: request.text })
        })
            .then(response => response.json())
            .then(data => {
                // Send the summary back to the content script
                sendResponse(data);
                // chrome.tabs.sendMessage(sender.tab.id, { action: "displaySummary", summary: data.summary });
            });
    }
    if (request.action === "getTNC"){
        console.log(request.linktofetch);
        fetch(linktofetch, {
            method: "GET",
            headers: { "Content-Type": "text/html" }
        }).then(res => res.text())
        .then(text =>  new DOMParser().parseFromString(text, 'text/html') )
        .then(document => {
            const childTermsElements = document.querySelectorAll('h1, h2, h3, p, div, code, span');
            let childTermText = '';
            childTermsElements.forEach(childElement => {
                const childText = childElement.innerText.toLowerCase();
                if (childText.includes('terms') || childText.includes('conditions') || childText.includes('privacy') || childText.includes('cookies')) {
                    childTermText += childElement.innerText + '\n';
                }
                
            });
            console.log(childTermText);
            sendResponse(childTermText);
        });
    }
    return true;
});
