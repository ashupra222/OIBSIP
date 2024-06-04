function createCustomPizza() {
    const baseTypeSelect = document.getElementById('base-type');
    const baseType = baseTypeSelect.options[baseTypeSelect.selectedIndex].text;
    const basePrice = parseFloat(baseTypeSelect.value.split(' ($')[1].split(')')[0]);

    const toppingElements = document.querySelectorAll('input[name="topping"]:checked');
    const toppings = Array.from(toppingElements).map(el => el.value);
    const toppingsCount = toppings.length;
    const toppingsPrice = toppingsCount * 1.00;

    const totalPrice = basePrice + toppingsPrice;

    let result = `<h3>Your Custom Pizza</h3>`;
    result += `<p>Base: ${baseType}</p>`;
    result += `<p>Toppings: ${toppings.join(', ') || 'None'}</p>`;
    result += `<p>Total Price: $${totalPrice.toFixed(2)}</p>`;

    document.getElementById('custom-pizza-result').innerHTML = result;
}
