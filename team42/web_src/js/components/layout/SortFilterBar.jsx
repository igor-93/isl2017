import React from 'react';
import FAIcon from "../icons/FAIcon";

/**
 * Component which display sort and filter buttons. Items, can be passed along with sort and filter functions,
 * a callback returns the updated list on change.
 *
 * Sort functions are assumed to sort ascending
 */
export default class SortFilterBar extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            sortOrder: SortFilterBar.SORT.ASC,
            activeFilters: []
        }
    }

    _renderFilters() {
        return this.props.filters.map((filter, idx) => {
            const isActive = this.state.activeFilters.indexOf(filter) >= 0;
            return <button className={'no-margin small button ' + (isActive ? '' : 'hollow')} key={idx} onClick={() => this._toggleFilter(filter)} >{filter.displayName}</button>
        });
    }

    _toggleFilter(filter) {
        const activeIdx = this.state.activeFilters.indexOf(filter);
        let nextActiveFilters = this.state.activeFilters.concat([]);
        if (activeIdx >= 0) {
            nextActiveFilters.splice(activeIdx, 1);
        } else {
            nextActiveFilters.push(filter);
        }
        const newState = Object.assign({}, this.state, {activeFilters: nextActiveFilters});
        this._returnItemFunc(newState);
        this.setState(newState);
    }

    _toggleSort() {
        const newOrder = this.state.sortOrder === SortFilterBar.SORT.ASC ? SortFilterBar.SORT.DESC : SortFilterBar.SORT.ASC;
        const newState = Object.assign({}, this.state, {sortOrder: newOrder});
        this._returnItemFunc(newState);
        this.setState(newState);
    }

    _renderSort() {
        if (this.props.sortFunc) {
            return <button className="no-margin small button" onClick={() => this._toggleSort()}><FAIcon iconName={'sort-' + this.state.sortOrder}/></button>
        } else {
            return null;
        }
    }

    _returnItemFunc(state) {
        const func = (items) => {
            let result = items;
            state.activeFilters.forEach((filterObj) => {
                result = result.filter(filterObj.filterFunc);
            });
            if (this.props.sortFunc) {
                if (state.sortOrder === SortFilterBar.SORT.ASC) {
                    result = result.sort(this.props.sortFunc);
                } else {
                    result = result.sort((i0, i1) => this.props.sortFunc(i1, i0));
                }
            }
            return result;
        };
        this.props.onItemFuncChanged(func);
    }

    render() {
        return (
            <div className="sort-filter-bar">
                <div className="filters">
                    {this._renderFilters()}
                </div>
                <div className="sorters">
                    {this._renderSort()}
                </div>
            </div>
        );
    }

}

SortFilterBar.propTypes = {
    sortFunc: React.PropTypes.func,
    filters: React.PropTypes.arrayOf(React.PropTypes.shape({
        displayName: React.PropTypes.node,
        name: React.PropTypes.string.isRequired, // unique name as identifier
        filterFunc: React.PropTypes.func.isRequired
    })),
    onItemFuncChanged: React.PropTypes.func
};

SortFilterBar.defaultProps = {
    onItemFuncChanged: () => {},
    filters: [],
    sortFunc: null
};

SortFilterBar.displayName = 'SortFilterBar';

SortFilterBar.SORT = {
    ASC: 'asc',
    DESC: 'desc'
};