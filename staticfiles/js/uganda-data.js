/**
 * Simplified Uganda Administrative Data
 * Based on Electoral Commission data
 */

const UGANDA_DATA = {
    "districts": [
        "Abim", "Adjumani", "Agago", "Alebtong", "Amolatar", "Amudat", "Amuria", "Amuru",
        "Apac", "Arua", "Budaka", "Bududa", "Bugiri", "Bugweri", "Buhweju", "Buikwe",
        "Bukedea", "Bukomansimbi", "Bukwo", "Bulambuli", "Buliisa", "Bundibugyo",
        "Bushenyi", "Busia", "Butaleja", "Butambala", "Butebo", "Buvuma", "Buyende",
        "Dokolo", "Gomba", "Gulu", "Hoima", "Ibanda", "Iganga", "Isingiro", "Jinja",
        "Kaabong", "Kabale", "Kabarole", "Kaberamaido", "Kagadi", "Kakumiro", "Kalaki",
        "Kalangala", "Kaliro", "Kalungu", "Kampala", "Kamuli", "Kamwenge", "Kanungu",
        "Kapchorwa", "Kapelebyong", "Karenga", "Kasanda", "Kasese", "Katakwi", "Kayunga",
        "Kazo", "Kibaale", "Kiboga", "Kibuku", "Kikuube", "Kiruhura", "Kiryandongo",
        "Kisoro", "Kitgum", "Koboko", "Kole", "Kotido", "Kumi", "Kwania", "Kween",
        "Kyankwanzi", "Kyegegwa", "Kyenjojo", "Kyotera", "Lamwo", "Lira", "Luuka",
        "Luwero", "Lwengo", "Lyantonde", "Manafwa", "Maracha", "Masaka", "Masindi",
        "Mayuge", "Mbale", "Mbarara", "Mitooma", "Mityana", "Moroto", "Moyo", "Mpigi",
        "Mubende", "Mukono", "Nabilatuk", "Nakapiripirit", "Nakaseke", "Nakasongola",
        "Namayingo", "Namisindwa", "Namutumba", "Napak", "Nebbi", "Ngora", "Noroko",
        "Ntoroko", "Ntungamo", "Nwoya", "Obongi", "Omoro", "Otuke", "Oyam", "Pader",
        "Pakwach", "Pallisa", "Rakai", "Rubanda", "Rubirizi", "Rukiga", "Rukungiri",
        "Sembabule", "Serere", "Sheema", "Sironko", "Soroti", "Tororo", "Wakiso",
        "Yumbe", "Zombo"
    ],
    "counties": {
        "Kampala": ["Kampala Central", "Nakawa", "Makindye", "Rubaga", "Kawempe"],
        "Wakiso": ["Kyadondo", "Busiro", "Entebbe"],
        "Mukono": ["Mukono Central", "Nakifuma"],
        "Jinja": ["Jinja Municipality", "Kagoma"],
        "Mbale": ["Mbale Municipality", "Bubulo"],
        "Gulu": ["Gulu Municipality", "Omoro", "Kilak"],
        "Mbarara": ["Mbarara Municipality", "Kashari"],
        "Arua": ["Arua Central", "Terego", "Ayivu"],
        "Lira": ["Lira Municipality", "Erute"],
        "Soroti": ["Soroti Municipality", "Dakabela"],
        "Kabale": ["Kabale Municipality", "Nkore", "Rubanda"],
        "Masaka": ["Masaka Municipality", "Bukoto"],
        "Tororo": ["Tororo Municipality", "West Budama", "Tororo North"],
        "Busia": ["Samia-Bugwe"],
        "Hoima": ["Bugahya"],
        "Kasese": ["Bukonzo", "Busongora"],
        "Fort Portal": ["Mwenge"],
        "Mubende": ["Kasanda"],
        "Luwero": ["Katikamu"],
        "Kayunga": ["Kayunga Central"],
        "Mityana": ["Mityana Central"],
        "Kiboga": ["Kiboga Central"],
        "Kyankwanzi": ["Kyankwanzi Central"]
    },
    "subcounties": {
        "Kampala Central": ["Kampala Central Division", "Kawempe Division", "Makindye Division", "Nakawa Division", "Rubaga Division"],
        "Nakawa": ["Nakawa", "Kyambogo", "Naguru", "Bukoto", "Kisaasi"],
        "Makindye": ["Makindye", "Kabalagala", "Nsambya", "Ggaba", "Lukuli"],
        "Kyadondo": ["Wakiso", "Nansana", "Kira", "Kasangati", "Gayaza", "Bweyogerere"],
        "Busiro": ["Entebbe", "Kajjansi", "Ssisa", "Nabweru", "Nangabo", "Masulita"],
        "Mukono Central": ["Mukono Town", "Goma", "Nakisunga", "Kyetume", "Seeta"],
        "Nakifuma": ["Nakifuma", "Kasawo", "Nagojje", "Kimenyedde"],
        "Jinja Municipality": ["Jinja Central", "Masese", "Walukuba", "Mpumudde", "Bugembe"],
        "Kagoma": ["Busede", "Buyengo", "Butagaya", "Budondo"],
        "Tororo Municipality": ["Tororo Central", "Northern", "Southern", "Eastern"],
        "West Budama": ["West Budama", "Mulanda", "Nagongera", "Kwapa"]
    }
};

// Make it globally available
window.UGANDA_DATA = UGANDA_DATA;
console.log('✅ Uganda data loaded:', UGANDA_DATA.districts.length, 'districts');