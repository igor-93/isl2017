import React from 'react';

export default class ContentBox extends React.Component {

    _renderActions() {
        if (this.props.actions.length === 0) {
            return null;
        }
        const actionsRendered = [];
        this.props.actions.forEach((action, idx) => {
           const actionCss = 'small button content-box-action ' + (action.className ? action.className : '');
           const actionTitle = action.description || null;
           if (typeof action.onClick === 'function') {
               actionsRendered.push((
                   <button key={idx} onClick={action.onClick} title={actionTitle} className={actionCss}>
                       {action.display}
                   </button>
               ));
           } else if (action.href) {
               actionsRendered.push((
                   <a target="_blank" key={idx} href={action.href} title={actionTitle} className={actionCss}>
                       {action.display}
                   </a>
               ));
           }
        });
        return (
            <div className="content-box-action-list">
                {actionsRendered}
            </div>
        );
    }


    render() {
        let className = 'content-box ';
        if (!this.props.title && ! this.props.headerRight) {
            className += 'no-header '
        }
        className += this.props.className;
        return (
            <div className={className}>
                <div className="content-box-header">
                    <span className="content-box-header-title">{this.props.title}</span>
                    <span className="content-box-header-right">{this.props.headerRight}</span>
                </div>
                <div className="content-box-content">
                    {this.props.children}
                </div>
                {this._renderActions()}
            </div>
        );
    }

}

ContentBox.propTypes = {
    children: React.PropTypes.node,
    title: React.PropTypes.string,
    headerRight: React.PropTypes.node,
    className: React.PropTypes.string,
    actions: React.PropTypes.arrayOf(React.PropTypes.shape(
        {
            onClick: React.PropTypes.func,
            href: React.PropTypes.string,
            display: React.PropTypes.node.isRequired,
            className: React.PropTypes.string,
            description: React.PropTypes.string
        }
    ))
};

ContentBox.defaultProps = {
    className: '',
    title: null,
    headerRight: null,
    actions: []
};

ContentBox.displayName = 'ContentBox';