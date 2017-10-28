import React from 'react';

import  * as spinnerStyles from '../../styles/loading-spinner.scss';

export default class LoadingSpinner extends React.Component {

    render() {
        return (
            <div className={'horizontal-spinner ' + (this.props.fullHeight ? 'full-height' : '') + (this.props.absoluteCover ? 'cover-absolute' : '')}>
                <div className="bounce1"></div>
                <div className="bounce2"></div>
                <div className="bounce3"></div>
            </div>
        );
    }

}

LoadingSpinner.propTypes = {
    fullHeight: React.PropTypes.bool,
    absoluteCover: React.PropTypes.bool
};

LoadingSpinner.defaultProps = {
    fullHeight: false
};

LoadingSpinner.displayName = 'LoadingSpinner';

    
    
