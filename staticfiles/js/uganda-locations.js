/**
 * Uganda Administrative Locations Handler
 * Using the ug-locations package from CDN
 */

// Wait for the library to be ready
function waitForUg() {
    return new Promise((resolve) => {
        if (window.ug) {
            resolve(window.ug);
        } else {
            window.addEventListener('ug-locations-ready', () => {
                resolve(window.ug);
            }, { once: true });
            
            // Timeout after 5 seconds
            setTimeout(() => {
                if (!window.ug) {
                    console.error('Timeout waiting for ug-locations');
                    resolve(null);
                }
            }, 5000);
        }
    });
}

document.addEventListener('DOMContentLoaded', async function() {
    console.log('Waiting for ug-locations...');
    const ug = await waitForUg();
    
    if (!ug) {
        console.error('❌ ug-locations library failed to load');
        return;
    }
    
    console.log('✅ ug-locations loaded successfully');
    initializeUgandaDropdowns(ug);
});

function initializeUgandaDropdowns(ug) {
    const districtSelect = document.getElementById('district');
    const countySelect = document.getElementById('county');
    const subcountySelect = document.getElementById('subcounty');
    
    if (!districtSelect || !countySelect || !subcountySelect) {
        console.log('Uganda dropdown elements not found');
        return;
    }
    
    // Populate districts
    populateDistricts(districtSelect, ug);
    
    // Handle district change
    districtSelect.addEventListener('change', function() {
        const districtName = this.value ? this.options[this.selectedIndex].text : '';
        if (districtName) {
            populateCounties(countySelect, ug, districtName);
            resetSubcounties(subcountySelect);
        } else {
            resetCounties(countySelect);
            resetSubcounties(subcountySelect);
        }
    });
    
    // Handle county change
    countySelect.addEventListener('change', function() {
        const districtName = districtSelect.options[districtSelect.selectedIndex]?.text || '';
        const countyName = this.options[this.selectedIndex]?.text || '';
        if (districtName && countyName) {
            populateSubcounties(subcountySelect, ug, districtName, countyName);
        } else {
            resetSubcounties(subcountySelect);
        }
    });
}

function populateDistricts(selectElement, ug) {
    selectElement.innerHTML = '<option value="">-- Select District --</option>';
    
    try {
        // Get districts from the library
        const districts = ug.getDistricts ? ug.getDistricts() : [];
        
        if (!districts || districts.length === 0) {
            console.warn('No districts found');
            useFallbackDistricts(selectElement);
            return;
        }
        
        districts.sort().forEach(district => {
            const option = document.createElement('option');
            option.value = district.toLowerCase().replace(/\s+/g, '_');
            option.textContent = district;
            selectElement.appendChild(option);
        });
        
        console.log(`✅ Loaded ${districts.length} districts`);
    } catch (error) {
        console.error('Error loading districts:', error);
        useFallbackDistricts(selectElement);
    }
}

function populateCounties(selectElement, ug, districtName) {
    selectElement.innerHTML = '<option value="">-- Select County --</option>';
    selectElement.disabled = false;
    
    try {
        // Get subcounties (counties) for the district
        const counties = ug.getSubcountiesInDistrict ? ug.getSubcountiesInDistrict(districtName) : [];
        
        if (!counties || counties.length === 0) {
            console.warn(`No counties found for ${districtName}`);
            useFallbackCounties(selectElement, districtName);
            return;
        }
        
        counties.sort().forEach(county => {
            const option = document.createElement('option');
            option.value = county.toLowerCase().replace(/\s+/g, '_');
            option.textContent = county;
            selectElement.appendChild(option);
        });
        
        console.log(`✅ Loaded ${counties.length} counties for ${districtName}`);
    } catch (error) {
        console.error('Error loading counties:', error);
        useFallbackCounties(selectElement, districtName);
    }
}

function populateSubcounties(selectElement, ug, districtName, countyName) {
    selectElement.innerHTML = '<option value="">-- Select Sub-county --</option>';
    selectElement.disabled = false;
    
    try {
        // Get parishes (subcounties) for the county
        const subcounties = ug.getParishesInSubcounty ? ug.getParishesInSubcounty(districtName, countyName) : [];
        
        if (!subcounties || subcounties.length === 0) {
            console.warn(`No subcounties found for ${countyName}`);
            useFallbackSubcounties(selectElement);
            return;
        }
        
        subcounties.sort().forEach(subcounty => {
            const option = document.createElement('option');
            option.value = subcounty.toLowerCase().replace(/\s+/g, '_');
            option.textContent = subcounty;
            selectElement.appendChild(option);
        });
        
        console.log(`✅ Loaded ${subcounties.length} subcounties for ${countyName}`);
    } catch (error) {
        console.error('Error loading subcounties:', error);
        useFallbackSubcounties(selectElement);
    }
}

function resetCounties(selectElement) {
    selectElement.innerHTML = '<option value="">-- Select County --</option>';
    selectElement.disabled = true;
}

function resetSubcounties(selectElement) {
    selectElement.innerHTML = '<option value="">-- Select Sub-county --</option>';
    selectElement.disabled = true;
}

// Fallback data in case the library fails
function useFallbackDistricts(selectElement) {
    const districts = [
        'Kampala', 'Wakiso', 'Mukono', 'Jinja', 'Mbale', 'Gulu', 
        'Mbarara', 'Arua', 'Lira', 'Soroti', 'Kabale', 'Masaka',
        'Fort Portal', 'Tororo', 'Busia', 'Hoima', 'Kasese'
    ];
    
    districts.sort().forEach(district => {
        const option = document.createElement('option');
        option.value = district.toLowerCase().replace(/\s+/g, '_');
        option.textContent = district;
        selectElement.appendChild(option);
    });
}

function useFallbackCounties(selectElement, districtName) {
    const counties = {
        'Kampala': ['Kampala Central', 'Nakawa', 'Makindye', 'Rubaga', 'Kawempe'],
        'Wakiso': ['Kyadondo', 'Busiro', 'Entebbe'],
        'Mukono': ['Mukono Central', 'Nakifuma'],
        'Jinja': ['Jinja Municipality', 'Kagoma'],
        'Tororo': ['Tororo Municipality', 'West Budama', 'Tororo North']
    };
    
    const list = counties[districtName] || ['County 1', 'County 2'];
    list.forEach(county => {
        const option = document.createElement('option');
        option.value = county.toLowerCase().replace(/\s+/g, '_');
        option.textContent = county;
        selectElement.appendChild(option);
    });
}

function useFallbackSubcounties(selectElement) {
    const subcounties = ['Sub-county 1', 'Sub-county 2', 'Sub-county 3'];
    subcounties.forEach(subcounty => {
        const option = document.createElement('option');
        option.value = subcounty.toLowerCase().replace(/\s+/g, '_');
        option.textContent = subcounty;
        selectElement.appendChild(option);
    });
}