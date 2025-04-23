function toggleAccordion(header) {
    const item = header.parentNode;
    const content = item.querySelector('.accordion-content');
    const allItems = document.querySelectorAll('.accordion-item');

    allItems.forEach(function (otherItem) {
        if (otherItem !== item) {
            otherItem.classList.remove('active');
            otherItem.querySelector('.accordion-content').style.maxHeight = null;
        }
    });

    item.classList.toggle('active');
    if (item.classList.contains('active')) {
        content.style.maxHeight = content.scrollHeight + "px";
    } else {
        content.style.maxHeight = null;
    }
}
