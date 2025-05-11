let termsText = '';
let childTermsText = '';

// Target elements like headings and paragraphs that may contain terms and conditions
const termsElements = document.querySelectorAll('h1, h2, h3, p, div, code, span');
termsElements.forEach(element => {
    const text = element.innerText.toLowerCase();
    if (text.includes('terms') || text.includes('conditions') || text.includes('privacy') || text.includes('cookies')) {
        if(element.tagName == 'DIV'){
            const links = Array.from(element.querySelectorAll('a')).filter(a => /terms|cookie|cookies|conditions|privacy|legal|policy|policies|more/i.test(a.textContent || a.href));
            linksDone = [];
            if (links.length > 0){
                links.forEach(link => {
                    if (linksDone.indexOf(link.href) == -1){
                        console.log(link.href);
                        chrome.runtime.sendMessage({action: "getTNC", linktofetch: link.href}, data => {childTermsText = data});
                        linksDone += link.href;
                    }
                });

            }
        }
        termsText += element.innerText + '\n';
    }
});

// console.log(childTermsText);
// Send extracted text to background script for summarization

chrome.runtime.onMessage.addListener(
    function (request, sender, sendResponse) {
        if (request.from === "popup") {
            if (termsText) {
                chrome.runtime.sendMessage({ action: "summarize", text: termsText }, r => {console.log(r);sendResponse(r);});
            } else {
                chrome.runtime.sendMessage({ action: "summarize", text: 'No terms and conditions found.' }, r => {console.log(r);sendResponse(r);});
            }
            
        }
        return true;
    }
);

chrome.runtime.onMessage.addListener(
    function (request, sender, sendResponse) {
        if (request.from === "content") {
            childTermsText = request.data;
        }
    }
);