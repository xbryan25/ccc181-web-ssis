
export function formatForYearLevelDonutChart(data: {yearLevel: string, count: number}[]){
    const formattedData = []
    
    for (const i in data) {
        formattedData.push({ label: data[i]?.yearLevel, value: data[i]?.count });
    }

    return formattedData
}

export function formatForGenderDonutChart(data: {gender: string, count: number}[]){
    const formattedData = []
    
    for (const i in data) {
        const gender = data[i]?.gender || '';

        formattedData.push({ label: (gender[0] ? gender[0].toUpperCase() : '') + gender.slice(1).toLowerCase(), value: data[i]?.count });
    }

    return formattedData
}
