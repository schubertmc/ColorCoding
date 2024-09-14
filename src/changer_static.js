//changer_static.js
// 2022-2024 Marc Schubert <schubert.mc.ai@gmail.com>

console.log("Starting static changer");
var word_data;

function initializeWithData(data, fontWeight) {
    word_data = data;
    let wordMap = new Map(word_data.map(item => [item.word.toLowerCase(), item]));
    colorizeWords(editableElement.shadowRoot.querySelector('anki-editable'), wordMap, fontWeight);
    placeCaretAtEnd(editableElement.shadowRoot.querySelector('anki-editable'));
}



var editableElement = document.activeElement;


function escapeRegExp(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

// Function to retrieve all text nodes within an element
function getAllTextNodes(element) {
    let textNodes = [];
    let walker = document.createTreeWalker(element, NodeFilter.SHOW_TEXT, null, false);
    let node;

    while ((node = walker.nextNode())) {
        textNodes.push(node);
    }
    return textNodes;
}

// Function to retrieve all nodes within an element
function getAllNodes(element) {
    let allNodes = [];
    let walker = document.createTreeWalker(element, NodeFilter.SHOW_ALL, null, false);
    let node;

    while ((node = walker.nextNode())) {
        allNodes.push(node);
    }
    return allNodes;
}


function colorizeWords(editableElement, wordMap, fontWeight) {

    console.log("Starting colorize words");
    removeAllColorCodingSpans(editableElement);

    const textNodes = getAllTextNodes(editableElement);
    textNodes.forEach(node => {
        let nodeContent = node.textContent;
        let fragment = document.createDocumentFragment();
        let words = nodeContent.split(/(\W)/)

        count = 0;

        for (let word_idx = 0; word_idx < words.length; word_idx++) {
            const cur_word = words[word_idx];
            
            let matched_item = wordMap.get(cur_word.toLowerCase());

            if (matched_item) {
                // item matched; now add the code
                //console.log("MATCH: ", matched_item.word);
                // create span element
                let span = document.createElement('span');
                span.style.color = matched_item.color;
                span.style.fontWeight = fontWeight;
                span.textContent = cur_word;
                span.className = 'ColorCoding';
                span.dataset.name = cur_word;
                span.dataset.group = matched_item.group;
                fragment.appendChild(span);


            } else {
                // word not matched - add as normal text
                //console.log("NOTmatched: ",cur_word );
                fragment.appendChild(document.createTextNode(cur_word));
                //console.log("Added as text node: ",cur_word );

            }


        }

        node.parentNode.replaceChild(fragment, node);
        


    });
}


function placeCaretAtEnd(el) {
    el.focus();
    if (typeof window.getSelection != "undefined"
        && typeof document.createRange != "undefined") {
        var range = document.createRange();
        range.selectNodeContents(el);
        range.collapse(false);
        var sel = window.getSelection();
        sel.removeAllRanges();
        sel.addRange(range);
    } else if (typeof document.body.createTextRange != "undefined") {
        var textRange = document.body.createTextRange();
        textRange.moveToElementText(el);
        textRange.collapse(false);
        textRange.select();
    }
}



function removeAllColorCodingSpans(editableElement) {
    const spans = editableElement.querySelectorAll('.ColorCoding');
    spans.forEach(span => {
        const parent = span.parentNode;
        // Move all child nodes of the span back to the parent node just before the span
        while (span.firstChild) {
            parent.insertBefore(span.firstChild, span);
        }
        // Remove the span from the DOM
        parent.removeChild(span);
    });
}
