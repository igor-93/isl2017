import React from 'react';

export default class Columns extends React.Component {

    render() {
        let colClasses = '';
        Columns.BREAKPOINTS.forEach((bp, idx) => {
            if (this.props.cols[idx]) {
                colClasses += ' ' + bp + '-' + this.props.cols[idx];
            }
        });
        return (
            <div className={'columns ' + colClasses + ' ' + this.props.className}>
                {this.props.children}
            </div>
        );
    }

}

Columns.propTypes = {
    children: React.PropTypes.node,
    cols: React.PropTypes.array,
    className: React.PropTypes.string
};

Columns.defaultProps = {
    cols: [12],
    className: React.PropTypes.string
};

Columns.displayName = 'Columns';

Columns.BREAKPOINTS = ['small', 'medium', 'large'];