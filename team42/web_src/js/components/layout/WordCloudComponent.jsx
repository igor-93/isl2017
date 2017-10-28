import React from 'react';
import WordCloud from "wordcloud"

export default class WordCloudComponent extends React.Component {

    componentDidMount() {
        this._drawWordCloud();
    }

    componentDidUpdate() {
        this._drawWordCloud();
    }

    _onWordCloudClick(item, dim, event) {
        this.props.onItemClick(item, dim, event);
    }

    _onWordCloudHover(item, dim, event) {
        this.props.onItemHover(item, dim, event);
    }

    _drawWordCloud() {
            WordCloud(document.getElementById(this.props.canvasId), {
                list: this.props.list,
                minSize:1,
                click: (item, dim, event) => this._onWordCloudClick(item, dim, event),
                hover: (item, dim, event) => this._onWordCloudHover(item, dim, event)
            });
    }

    _renderEmptyListMsg() {
        if (!this.props.list || this.props.list.length === 0) {
            return <span className="word-cloud-empty-msg">{this.props.emptyListMsg}</span>
        }
        return null;
    }

    render() {
        return (
            <div className="word-cloud-container">
                <canvas id={this.props.canvasId} />
                {this._renderEmptyListMsg()}
            </div>
        );
    }

}

WordCloudComponent.propTypes = {
    canvasId: React.PropTypes.string.isRequired,
    list: React.PropTypes.array,
    emptyListMsg: React.PropTypes.string,
    onItemClick: React.PropTypes.func,
    onItemHover: React.PropTypes.func
};

WordCloudComponent.defaultProps = {
    list: [],
    emptyListMsg: '',
    onItemClick: () => {},
    onItemHover: () => {}
};

WordCloudComponent.displayName = 'WordCloudComponent';