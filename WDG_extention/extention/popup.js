// chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
//     if (request.action === "displaySummary") {
//         console.log("from bg");
//         document.getElementById('summary').innerText = request.summary;
//     }
//     else if (request.action === 'summarize') {
//         console.log("true");
//     }
//     else {
//         console.log("a message caught");
//     }
// });

const setDOMInfo = (info) => {
  console.log(info);
  document.getElementById('summary').innerText = info.summary;
};

chrome.tabs.query({
  active: true,
  currentWindow: true
}, tabs => {
  // ...and send a request for the DOM info...
  console.log(tabs[0].id);
  chrome.tabs.sendMessage(
    tabs[0].id,
    { from: 'popup', subject: 'summary' },
    // ...also specifying a callback to be called 
    //    from the receiving end (content script).
    data => {
      document.getElementById('summary').innerText = data.summary;
    });
});