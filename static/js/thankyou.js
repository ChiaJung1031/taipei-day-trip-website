var nextpage;
var getdata =false;

//網頁一載入
window.onload = function ()
{
    let index="index"
    checkuser(index);
    let number = location.href.split('?')[1].split('=')[1]; //訂單編號
    let req = new XMLHttpRequest();
    req.open("GET","/api/orders/"+number)
    req.send();
    req.onload = function()
    {
        let data = JSON.parse(this.response);
        console.log(data["data"])
        if(data["data"] != null)
        {
            let num=data["data"]["number"];
            let order = document.getElementById("ordernum");
            order.innerHTML="謝謝訂購！訂單編號為："+num;
        }
    }
}




