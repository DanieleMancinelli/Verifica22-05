document.addEventListener('DOMContentLoaded', () => {
    loadCountries();
});

function loadCountries() {
    fetch('/get_countries')
        .then(response => response.json())
        .then(data => {
            const countryList = document.getElementById('country-list');
            countryList.innerHTML = '<h2>Seleziona una Nazione</h2>';
            data.forEach(country => {
                const countryLink = document.createElement('a');
                countryLink.href = '#';
                countryLink.textContent = country;
                countryLink.addEventListener('click', () => loadCities(country));
                countryList.appendChild(countryLink);
                countryList.appendChild(document.createElement('br'));
            });
        });
}

function loadCities(country) {
    fetch(`/get_cities/${country}`)
        .then(response => response.json())
        .then(data => {
            const cityList = document.getElementById('city-list');
            cityList.innerHTML = '<h2>Seleziona una Città</h2>';
            Object.keys(data).forEach(city => {
                const cityLink = document.createElement('a');
                cityLink.href = '#';
                cityLink.textContent = `${city} (${data[city]})`;
                cityLink.addEventListener('click', () => loadCustomers(city));
                cityList.appendChild(cityLink);
                cityList.appendChild(document.createElement('br'));
            });
        });
}

function loadCustomers(city) {
    fetch(`/get_customers?city=${city}`)
        .then(response => response.json())
        .then(data => {
            const customerList = document.getElementById('customer-list');
            customerList.innerHTML = '<h2>Elenco Clienti</h2>';
            if (data.length > 0) {
                const table = document.createElement('table');
                const header = table.createTHead().insertRow();
                Object.keys(data[0]).forEach(key => {
                    const th = document.createElement('th');
                    th.textContent = key;
                    header.appendChild(th);
                });

                const tbody = table.createTBody();
                data.forEach(customer => {
                    const row = tbody.insertRow();
                    Object.values(customer).forEach(value => {
                        const cell = row.insertCell();
                        cell.textContent = value;
                    });
                });

                customerList.appendChild(table);
            } else {
                customerList.textContent = 'Nessun cliente trovato per questa città.';
            }
        });
}