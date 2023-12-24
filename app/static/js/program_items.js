function showDescription(item) {
    var item_description = item.getElementsByClassName('item-description')[0];
    item_description.classList.remove('hidden');
}

function hideDescription(event, item_description) {
    event.stopPropagation();
    item_description.classList.add('hidden');

}