/**
 * Load the complete Uganda data from ug-locations package
 * This uses the actual Electoral Commission data
 */

// Function to load the package
async function loadUgandaData() {
    try {
        // Dynamic import of the package
        const ug = await import('/static/js/ug-locations/ug-locations.js');
        console.log('✅ ug-locations package loaded');
        
        // Make it globally available
        window.ug = ug.default || ug;
        
        // Get all districts
        const districts = window.ug.getDistricts ? window.ug.getDistricts() : [];
        console.log(`📊 Total districts: ${districts.length}`);
        
        // Test with a sample district
        if (districts.length > 0) {
            const sampleDistrict = districts[0];
            console.log(`Sample district: ${sampleDistrict}`);
            
            // Get counties for this district
            const counties = window.ug.getSubcountiesInDistrict ? 
                window.ug.getSubcountiesInDistrict(sampleDistrict) : [];
            console.log(`Counties in ${sampleDistrict}: ${counties.length}`);
            
            if (counties.length > 0) {
                console.log(`Sample county: ${counties[0]}`);
                
                // Get subcounties
                const subcounties = window.ug.getParishesInSubcounty ?
                    window.ug.getParishesInSubcounty(sampleDistrict, counties[0]) : [];
                console.log(`Subcounties in ${counties[0]}: ${subcounties.length}`);
            }
        }
        
        // Dispatch event when ready
        window.dispatchEvent(new CustomEvent('ug-data-ready', { detail: window.ug }));
        
    } catch (error) {
        console.error('Error loading ug-locations:', error);
    }
}

// Start loading
loadUgandaData();