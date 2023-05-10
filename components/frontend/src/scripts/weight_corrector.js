const NETTO_DELTA = 30;
const WEIGHT_STEP = 20;
const CHUNK_SIZE = 20;

function set_netto(visits, netto) {
    let targetWeight = netto / visits.length;
    let currentTotal = visits.reduce((acc, c) => acc + c.netto, 0);
    for (let i = 0; i < visits.length; i += CHUNK_SIZE) {
        const chunk = visits.slice(i, i + CHUNK_SIZE);
        bulk_update(chunk, targetWeight * chunk.length);
    };
    currentTotal = visits.reduce((acc, c) => acc + c.netto, 0);
    let c = 0
    while (netto != currentTotal) {
        let diff = netto - currentTotal;
        let rIndex = Math.floor(Math.random() * visits.length);
        let visit = visits[rIndex];

        bulk_update([visit,], visit.netto + diff);
        currentTotal = visits.reduce((acc, c) => acc + c.netto, 0);
        c++
    }
    console.log(c)
    return visits
}

function bulk_update(visits, targetWeight) {
    let currentTotalWeight = visits.reduce((acc, c) => acc + c.netto, 0);
    let useStep = (targetWeight - currentTotalWeight) / visits.length;
    for (let visit of visits) {
        // let maxNetto = visit.max_weight - visit.tara;
        // if (visit.netto >= maxNetto) continue

        let netto = getRNetto(visit.netto + useStep - NETTO_DELTA, visit.netto + useStep + NETTO_DELTA)
        // if ((visit.netto + useStep) <= maxNetto) {
        //     netto = getRNetto(visit.netto + useStep - NETTO_DELTA, visit.netto + useStep + NETTO_DELTA)
        // } else {
        //     netto = getRNetto(maxNetto - NETTO_DELTA, maxNetto + NETTO_DELTA)
        // };
        updateVisit(visit, netto);
    }
}

function getRNetto(MIN, MAX) {
    let r = Math.floor((MIN / WEIGHT_STEP + Math.random() * (MAX - MIN) / WEIGHT_STEP)) * WEIGHT_STEP;
    return r;
};
function updateVisit(visit, netto) {
    if (netto <= 0) {
        return
    }
    visit.netto = netto;
    visit.brutto = visit.tara + visit.netto;
    visit.weight_out = visit.brutto
};

module.exports = set_netto
