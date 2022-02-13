

let tableheader = {{tableheader | safe}};
let tableBodyData= {{data | safe}};

function createHeader(table,headervalues){
    let tHead = table.createTHead();
    let trow = tHead.insertRow();
    for (val in headervalues){
        // console.log(headervalues[val]);
        let th =document.createElement('th');
        let text = document.createTextNode(headervalues[val]);
        th.appendChild(text);
        trow.appendChild(th);
    }
}

function createtableBody(table,data){
    for (element in data){
        let row = table.insertRow();
        for (key in data[element]){
            let cell = row.insertCell();
            let text = document.createTextNode(data[element][key]);
            cell.appendChild(text);
        }
    }
}

var tableContent = document.getElementById('customers');
createHeader(tableContent,tableheader);
createtableBody(tableContent,tableBodyData);