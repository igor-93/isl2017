import React from 'react';

export default class Icon extends React.Component {

    render() {
        let iconClass = '';
        iconClass += this.props.name + ' ';
        iconClass += this.props.iconClass;

        return (
            <svg className={'icon ' + this.props.svgClass}>
                <use className={iconClass} xlinkHref={'#' + this.props.name} style={this.props.iconStyle}/>
            </svg>
        );
    }

}

Icon.propTypes = {
    name: React.PropTypes.string,
    iconClass: React.PropTypes.string,
    iconStyle: React.PropTypes.object,
    svgClass: React.PropTypes.string

};

Icon.defaultProps = {
    name: 'dummyIcon',
    iconClass: '',
    svgClass: '',
    iconStyle: {}

};

Icon.displayName = 'Icon';

Icon.ICONS = {
    HEART: 'icon_heart',
    DANDLI: 'icon_dandli'
};