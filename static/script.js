const modal = document.querySelector(".modal");
const overlay = document.querySelector(".overlay");


//Opening Function
const openModal =()=>{
    console.log("open");
    modal.classList.add("active");
    overlay.classList.add("overlayactive");
}


//Closing Function
const closeModal =()=>{
    console.log("close");
    modal.classList.remove("active");
    overlay.classList.remove("overlayactive");
}