function click_download(){
    let keyword = document.getElementById("keyword").value;
    let numpage = document.getElementById("number").value;
    let folder_name = document.getElementById("folderpath").value;
    if(keyword == ''){
        alert("請輸入關鍵字");
    }
    else if(numpage == ''){
        alert("請輸入頁數");
    }
    else if(numpage < 1){
        alert("頁數至少大於等於1")
    }
    else if(folder_name == ''){
        alert("請輸入資料夾名稱");
    }
    else{
        alert("下載圖片中，請耐心等候");
    }
}