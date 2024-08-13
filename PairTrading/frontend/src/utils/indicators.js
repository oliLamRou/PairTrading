import { BollingerBands, SMA, VWAP, EMA } from 'technicalindicators'

export const IndicatorStyle = {
    SMA: {
        color: "purple",
        lineWidth: 1,
        priceLineVisible: false, 
        lastValueVisible: false, 
        crosshairMarkerVisible: false
    },
    BollingerBands:{
        upper:{
            color: "red",
            lineWidth: 1,
            priceLineVisible: false, 
            lastValueVisible: false, 
            crosshairMarkerVisible: false
        },
        middle:{
            color: "blue",
            lineWidth: 1,
            priceLineVisible: false, 
            lastValueVisible: false, 
            crosshairMarkerVisible: false
        },
        lower:{
            color: "green",
            lineWidth: 1,
            priceLineVisible: false, 
            lastValueVisible: false, 
            crosshairMarkerVisible: false
        },
    },
    TripleEMA:{
        first:{
            color: 'rgba(80, 160, 220, 0.8)', 
            lineWidth : 1, 
            priceLineVisible: false, 
            lastValueVisible: false, 
            crosshairMarkerVisible: false
        },
        second:{
            color: 'rgba(70, 100, 58, 0.8)', 
            lineWidth : 1, 
            priceLineVisible: false, 
            lastValueVisible: false, 
            crosshairMarkerVisible: false
        },
        third:{
            color: 'rgba(165, 72, 221, 0.8)', 
            lineWidth : 1, 
            priceLineVisible: false, 
            lastValueVisible: false, 
            crosshairMarkerVisible: false
        }
    },
    VWAP:{
        color: 'orange', lineWidth : 2, 
        lineStyle: 2, 
        priceLineVisible: false, 
        lastValueVisible: false, 
        crosshairMarkerVisible: false
    },
}

export class Indicators {
    static LW_BollingerBands(input){
        const close = input.values.map(candle => candle.close);
        const bbData = BollingerBands.calculate({period: input.period, values: close, stdDev: input.stdDev});
        bbData.splice(0, 0, ...Array(input.period-3).fill(0))

        const bbSeriesUpper = input.values.slice(2).map((candle, index) => ({
            time: candle.time,
            value: bbData[index].upper
        }))
        const bbSeriesMiddle = input.values.slice(2).map((candle, index) => ({
            time: candle.time,
            value: bbData[index].middle
        }))
        const bbSeriesLower = input.values.slice(2).map((candle, index) => ({
            time: candle.time,
            value: bbData[index].lower
        }))
    
        const outBBands = {
            upper: bbSeriesUpper,
            middle: bbSeriesMiddle,
            lower: bbSeriesLower
        }

        return outBBands
    }

    static LW_SMA(input){
        const close = input.values.map(candle => candle.close);
        const smaData = SMA.calculate({period: input.period, values: close});
        smaData.splice(0, 0, ...Array(input.period-3).fill(undefined))

        const smaSeries = input.values.slice(2).map((candle, index) => ({
            time: candle.time,
            value: smaData[index]
        }))

        return smaSeries
    }

    static LW_Volume(input){
        const vol = input.values.map(candle => candle.volume);
        const volSeries = input.values.slice(2).map((candle, index) => ({
            time: candle.time,
            value: vol[index]
        }))

        return volSeries
    }

    static LW_VWAP(input){
        const vwInput = {
            high: input.values.map(candle => candle.high),
            low: input.values.map(candle => candle.low),
            close: input.values.map(candle => candle.close),
            volume: input.values.map(candle => Math.round(candle.volume)),
            //volume: input.values.map(candle => Math.round((candle.value-20) * 100)), // TEMP volume, need to add it to series data
        };

        const vwapData = VWAP.calculate(vwInput);
        const vwapSeries = input.values.slice(2).map((candle, index) => ({
            time: candle.time,
            value: vwapData[index]
        }))
        return vwapSeries
    }

    static LW_TripleEMA(input){
        const close = input.values.map(candle => candle.close);
        const firstData = EMA.calculate({period: input.first, values: close});
        const secondData = EMA.calculate({period: input.second, values: close});
        const thirdData = EMA.calculate({period: input.third, values: close});

        firstData.splice(0, 0, ...Array(input.first-3).fill(undefined))
        secondData.splice(0, 0, ...Array(input.second-3).fill(undefined))
        thirdData.splice(0, 0, ...Array(input.third-3).fill(undefined))

        const firstEMA = input.values.slice(2).map((candle, index) => ({
            time: candle.time,
            value: firstData[index],
        }))
        const secondEMA = input.values.slice(2).map((candle, index) => ({
            time: candle.time,
            value: secondData[index],
        }))
        const thirdEMA = input.values.slice(2).map((candle, index) => ({
            time: candle.time,
            value: thirdData[index],
        }))

        const outEMA = {
            first: firstEMA,
            second: secondEMA,
            third: thirdEMA
        }

        return outEMA
    }
}
