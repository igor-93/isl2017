import React from 'react';

import statsBoxStyles from 'Styles/stats-box.scss';

export default class StatsBox extends React.Component {

    _showSign(num) {
        let signString = '';
        if (num > 0) {
            signString = '+';
        } else if (num < 0) {
            signString = '-';
        }

        return signString + this._formatNumber(Math.abs(num));
    }

    _formatNumber(num) {
        if (typeof num === 'string') {
            return num;
        }
        if (Number.isInteger(num)) {
            return String(num);
        } else {
            return Number(num).toFixed(2);
        }
    }

    render() {
        let hasChange = false;
        if (typeof this.props.change === 'number') {
            hasChange = true;
        }

        return (
            <div className={'stats-box ' + this.props.className}>
                <div className="stats-box-title">
                    {this.props.title}
                </div>
                <div className="stats-box-value">
                    {this._formatNumber(this.props.value)}
                </div>
                {hasChange &&
                <div className="stats-box-change">
                    {this._showSign(this.props.change)}
                </div>
                }
            </div>
        );
    }

}

StatsBox.propTypes = {
    title: React.PropTypes.string,
    value: React.PropTypes.oneOfType([React.PropTypes.string, React.PropTypes.number]),
    change: React.PropTypes.number,
    className: React.PropTypes.string
};

StatsBox.defaultProps = {
    className: ''
};

StatsBox.displayName = 'StatsBox';