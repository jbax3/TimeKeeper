document.onclick = ()=>{document.title = 'JupyterLab' + ' - ' + document.getElementsByClassName("jp-mod-current")[0].title.split('Name: ')[1].split('\n')[0]}