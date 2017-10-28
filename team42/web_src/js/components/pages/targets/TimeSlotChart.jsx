import React from 'react';

import slotStyles from '../../../../styles/timeslot-chart.scss';

export default class TimeSlotChart extends React.Component {

    _getTimeFooter() {
        const cells = [];

        const firstDay = this.props.timeSlots[Object.keys(this.props.timeSlots)[0]];

        if (firstDay) {

            Object.keys(firstDay).forEach((bucket, idx) => {
                let i_str = String(bucket);
                if (i_str.length === 1) {
                    i_str = '0' + i_str;
                }
                cells.push(<td className="column-header" key={bucket}><span>{i_str}</span></td>);
            });

            return (
                <tr>
                    <td className="column-header row-header"></td>
                    {cells}
                </tr>
            );
        } else {
            return <tr> </tr>;
        }
    }

    _renderHour(value, key) {
        return (
            <td key={key}>
                <div className="time-slot" style={{width: (value * 100 + '%'), height: (value * 100 + '%')}}>

                </div>
            </td>
        );
    }

    _renderDay(day, key) {
        const cells = [];

        Object.keys(day).forEach((key, idx) => {
            cells.push(this._renderHour(day[key], idx));
        });

        return (
            <tr key={key} >
                <td className="row-header">{TimeSlotChart.DAYS_SHORT[key]}</td>
                {cells}
            </tr>
        );
    }

    _applyTimezoneShift(timeSlots) {
        let weekHours = [];
        // first linearize the data structure
        for (let d = 0; d < 7; d++) {
            for (let h = 0; h < 24; h++) {
                const slotValue = timeSlots[d][Math.floor(h / 2) * 2];
                weekHours.push(slotValue / 2);
            }
        }
        // shift
        const timeDiff = (new Date().getTimezoneOffset()) / 60;
        const shift = weekHours.splice(timeDiff, Math.abs(timeDiff));
        if (timeDiff < 0) {
            weekHours = shift.concat(weekHours);
        } else {
            weekHours = weekHours.concat(shift);
        }
        // reassemble
        const shiftedTimeSlots = {};
        for (let d = 0; d < 7; d++) {
            shiftedTimeSlots[d] = {};
            for (let h = 0; h < 24; h+=2) {
                const idx = (24 * d) + h;
                shiftedTimeSlots[d][h] = weekHours[idx] + weekHours[idx + 1];
            }
        }
        return shiftedTimeSlots;
    }

    render() {
        const fullTimeSlots = this._applyTimezoneShift(this.props.timeSlots);
        // const fullTimeSlots = this.props.timeSlots;
        const rows = [];

        Object.keys(fullTimeSlots).forEach((dayNum) => {
            rows.push(this._renderDay(fullTimeSlots[dayNum], dayNum));
        });

        return (
            <div className="time-slot-chart">
                <table className="time-slot-chart-table">
                    <tbody>
                        {rows}
                        {this._getTimeFooter()}
                    </tbody>
                </table>
            </div>
        );
    }

}

TimeSlotChart.propTypes = {
    timeSlots: React.PropTypes.object
};

TimeSlotChart.defaultProps = {
    timeSlots: {}
};

TimeSlotChart.displayName = 'TimeSlotChart';

TimeSlotChart.DAYS_SHORT = ['Mo', 'Tue', 'Wed', 'Thu', 'Fr', 'Sa', 'Su'];