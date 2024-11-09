export const getFirstDayOfWeek = (d: Date) => {
    d = new Date(d);
    const day = d.getDay(),
        diff = d.getDate() - day + (day == 0 ? -6 : 1);
    return new Date(d.setDate(diff));
};

export const getLastDayOfWeek = (d: Date) => {
    d = getFirstDayOfWeek(d);
    d = new Date(d.setDate(d.getDate() + 6));
    d.setHours(23,59,59)
    return d
};

export const getDateWeek = (d: Date) => {
    const currentDate = d;
    const januaryFirst = new Date(currentDate.getFullYear(), 0, 1);
    const daysToNextMonday = januaryFirst.getDay() === 1 ? 0 : (7 - januaryFirst.getDay()) % 7;
    const nextMonday = new Date(currentDate.getFullYear(), 0, januaryFirst.getDate() + daysToNextMonday);

    return currentDate < nextMonday
        ? 52
        : currentDate > nextMonday
          ? Math.ceil((currentDate.getTime() - nextMonday.getTime()) / (24 * 3600 * 1000) / 7)
          : 1;
};
