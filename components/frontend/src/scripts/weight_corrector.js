const NETTO_DELTA = 30;
const WEIGHT_STEP = 20;
const CHUNK_SIZE = 20;

function set_netto(visits, netto, tonar = true) {
    if (netto % 20 !== 0) {
        netto = getRNetto(netto - 10, netto + 10)
    }
    let targetWeight = netto / visits.length;
    let currentTotal = visits.reduce((acc, c) => acc + c.netto, 0);

    var c = 0
    while (netto != currentTotal && c < 10) {
        for (let i = 0; i < visits.length; i += CHUNK_SIZE) {
            const chunk = visits.slice(i, i + CHUNK_SIZE);
            bulk_update(chunk, targetWeight * chunk.length, tonar);
        };
        let diff = netto - currentTotal;
        let rIndex = Math.floor(Math.random() * visits.length);
        let visit = visits[rIndex];

        bulk_update([visit,], visit.netto + diff, tonar);
        if (currentTotal == visits.reduce((acc, c) => acc + c.netto, 0)) {
            c++
            continue
        }
        currentTotal = visits.reduce((acc, c) => acc + c.netto, 0);
    }
    return visits
}

function bulk_update(visits, targetWeight, tonar = true) {
    let currentTotalWeight = visits.reduce((acc, c) => acc + c.netto, 0);
    let useStep = (targetWeight - currentTotalWeight) / visits.length;
    for (let visit of visits) {
        let maxNetto = visit.max_weight - visit.tara;
        if (visit.netto >= maxNetto) continue

        let netto = getRNetto(visit.netto + useStep - NETTO_DELTA, visit.netto + useStep + NETTO_DELTA)
        if ((visit.netto + useStep) <= maxNetto) {
            netto = getRNetto(visit.netto + useStep - NETTO_DELTA, visit.netto + useStep + NETTO_DELTA)
        } else {
            netto = getRNetto(maxNetto - NETTO_DELTA, maxNetto + NETTO_DELTA)
        };
        updateVisit(visit, netto, tonar);
    }
}

function incNetto(visits, target = null) {
    if (target !== null) {
        return set_netto(visits, target, false)
    } else {

        let visitsByTrucks = {}
        for (var visit of visits) {
            if (visit.reg_number in visitsByTrucks) {
                visitsByTrucks[visit.reg_number].push(visit)
            } else {
                visitsByTrucks[visit.reg_number] = Array(visit)
            }
        }

        let f = []
        for (var reg_number in visitsByTrucks) {
            var nettos = []
            visitsByTrucks[reg_number].forEach((x) => nettos.push(x.netto))
            var max = Math.max(...nettos)
            var target = nettos.reduce((a, b) => a + getRNetto(max - NETTO_DELTA, max), 0)

            for (let visit of visitsByTrucks[reg_number]) {
                if (visit.frozen) continue

                var maxNetto = visit.max_weight - visit.tara;
                var netto = getRNetto(max - NETTO_DELTA, max + NETTO_DELTA)
                if (visit.netto >= maxNetto) {
                    if (visit.netto % 20 !== 0) {
                        netto = getRNetto(netto - 10, netto + 10)
                    } else continue
                }
                visit = updateVisit(visit, netto, false);
                f.push(visit)
            }
        }
        return f
    }
}

function getRNetto(MIN, MAX) {
    let r = Math.floor((MIN / WEIGHT_STEP + Math.random() * (MAX - MIN) / WEIGHT_STEP)) * WEIGHT_STEP;
    return r;
};
function updateVisit(visit, netto, tonar = true) {
    if (netto <= 0) {
        return
    }
    visit.netto = netto;
    visit.brutto = visit.tara + visit.netto;
    if (tonar) {
        visit.weight_out = visit.brutto
    } else {
        visit.weight_in = visit.brutto
    }

    return visit
};

module.exports = { set_netto, incNetto }
