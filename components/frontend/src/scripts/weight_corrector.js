const NETTO_DELTA = 30;
const WEIGHT_STEP = 20;
const CHUNK_SIZE = 20;
const TOTAL_DIFF = 20000;
const MAX_NETTO = 15000

function set_netto(visits, netto, tonar = true) {
    if (netto % 20 !== 0) {
        netto = getRNetto(netto - 10, netto + 10)
    }
    let targetWeight = netto / visits.length;
    let currentTotal = visits.reduce((acc, c) => acc + c.netto, 0);
    for (let i = 0; i < visits.length; i += CHUNK_SIZE) {
        const chunk = visits.slice(i, i + CHUNK_SIZE);
        bulk_update(chunk, targetWeight * chunk.length, tonar);
    };
    var c = 0
    while (netto != currentTotal && c < 20) {
        for (let i = 0; i < visits.length; i += CHUNK_SIZE) {
            const chunk = visits.slice(i, i + CHUNK_SIZE);
            bulk_update(chunk, targetWeight * chunk.length, tonar);
        };
        c++
        // console.log(c)
        currentTotal = visits.reduce((acc, v) => acc + v.netto, 0);
    }
    // console.log(netto)
    // console.log(currentTotal)

    c = 0
    while (netto != currentTotal && c < 400) {
        let diff = netto - currentTotal;
        let rIndex = Math.floor(Math.random() * visits.length);
        let visit = visits[rIndex];

        bulk_update([visit,], visit.netto + diff, tonar);
        if (currentTotal == visits.reduce((acc, c) => acc + c.netto, 0)) {
            c++
            // console.log(c)
            continue
        }
        currentTotal = visits.reduce((acc, c) => acc + c.netto, 0);
    }
    return {
        visits: visits,
        count: visits.length
    }
}

function bulk_update(visits, targetWeight, tonar = true) {
    let currentTotalWeight = visits.reduce((acc, c) => acc + c.netto, 0);
    let useStep = (targetWeight - currentTotalWeight) / visits.length;
    for (let visit of visits) {
        let maxNetto = visit.max_weight - visit.tara;

        let netto = getRNetto(visit.netto + useStep - NETTO_DELTA, visit.netto + useStep + NETTO_DELTA)

        if (netto > maxNetto) {
            netto = getRNetto(maxNetto - NETTO_DELTA, maxNetto + NETTO_DELTA)
        };
        visit = updateVisit(visit, netto, tonar);
    }
}
function lessEffectInc(visits, target) {
    // console.log(`target = ${target}`)
    let i = 0
    let updatedVisits = []
    let totalWeight = visits.reduce((acc, c) => acc + c.netto, 0);
    // console.log(`totalWeight = ${totalWeight}`)
    if (target <= totalWeight) {
        return {
            visits: visits,
            count: i
        }
    }
    while (target > totalWeight && i < visits.length) {
        i++
        updatedVisits = changeWithMaxEffect(visits, target - totalWeight)
        totalWeight = updatedVisits.reduce((acc, c) => acc + c.netto, 0);
        // console.log(`totalWeight = ${totalWeight}`)
    }
    return {
        visits: updatedVisits,
        count: i
    }
};
function changeWithMaxEffect(visits, target) {
    let visitsByID = {}
    for (var visit of visits) {
        visitsByID[visit.id] = visit
    };

    let visitsByTrucks = {}
    for (var visit of visits) {
        if (visit.reg_number in visitsByTrucks) {
            visitsByTrucks[visit.reg_number].push(visit)
        } else {
            visitsByTrucks[visit.reg_number] = Array(visit)
        }
    };

    let effectsByTrucks = {}
    for (var reg_number in visitsByTrucks) {
        sortedByNetto = visitsByTrucks[reg_number].sort((a, b) => a.netto - b.netto);
        maxEffectVisit = sortedByNetto[0];
        minEffectVisit = sortedByNetto[sortedByNetto.length - 1];

        // console.log(`maxEffectVisit.netto = ${maxEffectVisit.netto}`)
        // console.log(`minEffectVisit.netto = ${minEffectVisit.netto}`)
        // console.log(`effect = ${minEffectVisit.netto - maxEffectVisit.netto}`)
        if (minEffectVisit.netto == maxEffectVisit.netto) {
            effectsByTrucks[minEffectVisit.netto - maxEffectVisit.netto] = maxEffectVisit
        } else {
            var maxNetto = maxEffectVisit.max_weight - maxEffectVisit.tara
            if (maxNetto > MAX_NETTO) {
                maxNetto = MAX_NETTO
            }
            effectsByTrucks[maxNetto - maxEffectVisit.netto] = maxEffectVisit
        }

    };
    let effects = Object.keys(effectsByTrucks);
    let minEffect = effects.sort((a, b) => a - b)[0]
    let maxEffect = effects.sort((a, b) => a - b)[effects.length - 1]
    // console.log(`maxEffect = ${maxEffect}`)
    // console.log(`minEffect = ${minEffect}`)
    // console.log(`target = ${target}`)
    if (target <= maxEffect) {
        var visit = effectsByTrucks[maxEffect]
        // console.log(`visit.netto = ${visit.netto}`)
        var t = parseInt(visit.netto) + parseInt(target)
        var netto = getRNetto(t - 10, t + 10)
        visitsByID[visit.id] = updateVisit(visit, netto, false)

        // console.log(`netto = ${netto}`)
        // console.log(`visit.id = ${visit.id}`)
        // console.log(`visit.invoice = ${visit.invoice}`)

    } else {
        var visit = effectsByTrucks[maxEffect]
        // console.log(`visit.netto = ${visit.netto}`)
        var t = parseInt(visit.netto) + parseInt(maxEffect)
        var netto = getRNetto(t - 10, t + 10)
        visitsByID[visit.id] = updateVisit(visit, netto, false)

        // console.log(`netto = ${netto}`)
        // console.log(`visit.id = ${visit.id}`)
        // console.log(`visit.invoice = ${visit.invoice}`)

    }
    return Object.values(visitsByID)
}

function incNetto(visits, target = null, lessVisits = false) {
    if (target !== null) {
        if (lessVisits === true) {
            return lessEffectInc(visits, target)
        } else {
            return set_netto(visits, target, false)
        }
    }

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
    return {
        visits: f,
        count: f.length
    }

}

function getRNetto(MIN, MAX) {
    // console.log(`MIN = ${MIN}`)
    // console.log(`MAX = ${MAX}`)
    let r = Math.floor((MIN / WEIGHT_STEP + Math.random() * (MAX - MIN) / WEIGHT_STEP)) * WEIGHT_STEP;
    return r;
};
function updateVisit(visit, netto, tonar = true) {
    if (netto <= 0) {
        return visit
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

module.exports = { set_netto, incNetto, lessEffectInc }
