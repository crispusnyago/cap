/**
 * Simple Uganda Locations Handler
 * Uses static data instead of external library
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('Initializing Uganda dropdowns with static data');
    
    const districtSelect = document.getElementById('district');
    const countySelect = document.getElementById('county');
    const subcountySelect = document.getElementById('subcounty');
    
    if (!districtSelect || !countySelect || !subcountySelect) {
        console.log('Dropdown elements not found');
        return;
    }
    
    // Wait for data to be available
    function initialize() {
        if (!window.UGANDA_DATA) {
            setTimeout(initialize, 100);
            return;
        }
        
        console.log('UGANDA_DATA found, populating districts');
        populateDistricts(districtSelect);
    }
    
    initialize();
    
    districtSelect.addEventListener('change', function() {
        const districtName = this.options[this.selectedIndex]?.text;
        if (districtName && districtName !== '-- Select District --') {
            populateCounties(countySelect, districtName);
            resetSubcounties(subcountySelect);
        } else {
            resetCounties(countySelect);
            resetSubcounties(subcountySelect);
        }
    });
    
    countySelect.addEventListener('change', function() {
        const districtName = districtSelect.options[districtSelect.selectedIndex]?.text;
        const countyName = this.options[this.selectedIndex]?.text;
        if (districtName && countyName && 
            districtName !== '-- Select District --' && 
            countyName !== '-- Select County --') {
            populateSubcounties(subcountySelect, countyName);
        } else {
            resetSubcounties(subcountySelect);
        }
    });
});

function populateDistricts(selectElement) {
    selectElement.innerHTML = '<option value="">-- Select District --</option>';
    
    const districts = window.UGANDA_DATA.districts || [];
    districts.sort().forEach(districtName => {
        const option = document.createElement('option');
        option.value = districtName.toLowerCase().replace(/\s+/g, '_');
        option.textContent = districtName;
        selectElement.appendChild(option);
    });
    
    console.log(`Loaded ${districts.length} districts`);
}

function populateCounties(selectElement, districtName) {
    selectElement.innerHTML = '<option value="">-- Select County --</option>';
    selectElement.disabled = false;
    
    const counties = window.UGANDA_DATA.counties[districtName] || [];
    
    if (counties.length === 0) {
        console.warn(`No counties found for ${districtName}`);
        const option = document.createElement('option');
        option.value = 'default';
        option.textContent = 'No counties available';
        selectElement.appendChild(option);
        return;
    }
    
    counties.sort().forEach(countyName => {
        const option = document.createElement('option');
        option.value = countyName.toLowerCase().replace(/\s+/g, '_');
        option.textContent = countyName;
        selectElement.appendChild(option);
    });
    
    console.log(`Loaded ${counties.length} counties for ${districtName}`);
}

function populateSubcounties(selectElement, countyName) {
    selectElement.innerHTML = '<option value="">-- Select Sub-county --</option>';
    selectElement.disabled = false;
    
    const subcounties = window.UGANDA_DATA.subcounties[countyName] || [];
    
    if (subcounties.length === 0) {
        console.warn(`No subcounties found for ${countyName}`);
        const option = document.createElement('option');
        option.value = 'default';
        option.textContent = 'No subcounties available';
        selectElement.appendChild(option);
        return;
    }
    
    subcounties.sort().forEach(subcountyName => {
        const option = document.createElement('option');
        option.value = subcountyName.toLowerCase().replace(/\s+/g, '_');
        option.textContent = subcountyName;
        selectElement.appendChild(option);
    });
    
    console.log(`Loaded ${subcounties.length} subcounties for ${countyName}`);
}

function resetCounties(selectElement) {
    selectElement.innerHTML = '<option value="">-- Select County --</option>';
    selectElement.disabled = true;
}

function resetSubcounties(selectElement) {
    selectElement.innerHTML = '<option value="">-- Select Sub-county --</option>';
    selectElement.disabled = true;
}