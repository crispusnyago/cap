/**
 * Real Uganda Locations Handler
 * Uses the actual Electoral Commission data from ug-locations
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('Waiting for Uganda data...');
    
    const districtSelect = document.getElementById('district');
    const countySelect = document.getElementById('county');
    const subcountySelect = document.getElementById('subcounty');
    
    if (!districtSelect || !countySelect || !subcountySelect) {
        console.error('Dropdown elements not found');
        return;
    }
    
    // Wait for data to be ready
    window.addEventListener('ug-data-ready', function(event) {
        console.log('✅ Uganda data ready, populating dropdowns');
        const ug = event.detail;
        
        // Populate districts
        populateDistricts(districtSelect, ug);
        
        // District change handler
        districtSelect.addEventListener('change', function() {
            const districtName = this.options[this.selectedIndex]?.text;
            if (districtName && districtName !== '-- Select District --') {
                populateCounties(countySelect, ug, districtName);
                resetSubcounties(subcountySelect);
            } else {
                resetCounties(countySelect);
                resetSubcounties(subcountySelect);
            }
        });
        
        // County change handler
        countySelect.addEventListener('change', function() {
            const districtName = districtSelect.options[districtSelect.selectedIndex]?.text;
            const countyName = this.options[this.selectedIndex]?.text;
            if (districtName && countyName && 
                districtName !== '-- Select District --' && 
                countyName !== '-- Select County --') {
                populateSubcounties(subcountySelect, ug, districtName, countyName);
            } else {
                resetSubcounties(subcountySelect);
            }
        });
    });
});

function populateDistricts(selectElement, ug) {
    selectElement.innerHTML = '<option value="">-- Select District --</option>';
    
    const districts = ug.getDistricts ? ug.getDistricts() : [];
    console.log(`📋 Loading ${districts.length} districts`);
    
    districts.sort().forEach(districtName => {
        const option = document.createElement('option');
        option.value = districtName.toLowerCase().replace(/\s+/g, '_');
        option.textContent = districtName;
        selectElement.appendChild(option);
    });
}

function populateCounties(selectElement, ug, districtName) {
    selectElement.innerHTML = '<option value="">-- Select County --</option>';
    selectElement.disabled = false;
    
    // Note: In ug-locations, subcounties are what we call counties in the hierarchy
    const counties = ug.getSubcountiesInDistrict ? 
        ug.getSubcountiesInDistrict(districtName) : [];
    
    console.log(`📋 Found ${counties.length} counties for ${districtName}`);
    
    if (counties.length === 0) {
        const option = document.createElement('option');
        option.value = 'none';
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
}

function populateSubcounties(selectElement, ug, districtName, countyName) {
    selectElement.innerHTML = '<option value="">-- Select Sub-county --</option>';
    selectElement.disabled = false;
    
    // In ug-locations, parishes are what we call subcounties
    const subcounties = ug.getParishesInSubcounty ? 
        ug.getParishesInSubcounty(districtName, countyName) : [];
    
    console.log(`📋 Found ${subcounties.length} subcounties for ${countyName}`);
    
    if (subcounties.length === 0) {
        const option = document.createElement('option');
        option.value = 'none';
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
}

function resetCounties(selectElement) {
    selectElement.innerHTML = '<option value="">-- Select County --</option>';
    selectElement.disabled = true;
}

function resetSubcounties(selectElement) {
    selectElement.innerHTML = '<option value="">-- Select Sub-county --</option>';
    selectElement.disabled = true;
}