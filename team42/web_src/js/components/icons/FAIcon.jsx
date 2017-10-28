import React from 'react';

import 'Styles/fa-icons.scss';

export default class FAIcon extends React.Component {

    render() {
        let cssClasses = 'fa ';
        cssClasses += 'fa-' + this.props.iconName + ' ';

        cssClasses += this.props.className;
        return (
            <span className={cssClasses} title={this.props.title} />
        );
    }

}

FAIcon.propTypes = {
    iconName: React.PropTypes.string,
    className: React.PropTypes.string,
    title: React.PropTypes.string
};

FAIcon.defaultProps = {
    iconName: 'circle',
    className: '',
    title: null
};

FAIcon.displayName = 'FAIcon';