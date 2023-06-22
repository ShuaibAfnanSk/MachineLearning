const sliders = document.querySelectorAll(".slide-in");
const appearOptions = {
    threshold: 0,
    rootMargin: "0px 0px -150px 0px"
};
const appearOnScroll = new IntersectionObserver(function (
    entries,
    appearOnScroll
) {
    entries.forEach(entry => {
        if (!entry.isIntersecting) {
            return;
        } else {
            entry.target.classList.add("show")
            appearOnScroll.unobserve(entry.target);
        }
    });
},
    appearOptions);

sliders.forEach(slider => {
    appearOnScroll.observe(slider);
});

var menu = document.getElementById("menu");
function openmenu(){
    menu.style.right = "0";
}

function closemenu(){
    menu.style.right = "-300px";
}

function btn(){
    menu.style.right = "-300px";
}




