import React from 'react';

import { connect } from 'react-redux';

import {FETCH_STATUS} from '../../../constants';

import {fetchUserSearchResults, trackUser} from '../../../store/actions';

import  * as searchStyles from '../../../../styles/search.scss';
import LoadingSpinner from "../../LoadingSpinner";
import InstaUserLink from "../../layout/InstaUserLink";

export default class UserSearch extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            showResults: false,
            searchInputValue: '',
            loading: false
        };

        this.autoSearchTimeout = null;
    }
    componentWillReceiveProps(nextProps) {
        this.setState({
            loading: nextProps.searchStatus === FETCH_STATUS.FETCHING
        });
    }

    _renderSearchResults() {
        if (this.state.loading) {
            return <LoadingSpinner/>;
        } else {
            return this.props.searchResults.slice(0, 10).map((result, idx) => {
                return <div className="hoverable search-bar-results-item" key={idx}>
                    <div className="search-bar-results-item-text">
                        <div className="user-search-result-username"><strong><InstaUserLink username={result.username}/></strong></div>
                        <div className="user-search-result-full">{result.full_name}</div>
                    </div>
                    <div className="search-bar-results-item-actions">
                        <button className="button list-action"
                                onClick={(e) => this._onAddUserButtonClick(e)}
                                data-username={result.username}>
                            Add
                        </button>
                    </div>

                </div>;
            });
        }


    }

    _onAddUserButtonClick(e) {
        this.props.addUser(e.target.dataset.username);
        this.setState({showResults: false, searchInputValue: ''});
    }

    _onInputFocus() {
        if (this.state.searchInputValue.length > 0) {
            this._showResults();
        }
    }

    _onSearchInputChange(e) {
        if (typeof this.autoSearchTimeout === 'number') {
            clearTimeout(this.autoSearchTimeout);
        }
        const show = e.target.value.length > 0;
        this.setState({searchInputValue: e.target.value, showResults: show});
        this.autoSearchTimeout = setTimeout(() => {
            this.props.startSearch(this.state.searchInputValue);
        }, 500);
    }

    _onOutsideClick() {
        this.setState({showResults: false, searchInputValue: ''});
    }

    _showResults() {
        this.setState({showResults: true});
    }

    _hideResults() {
        this.setState({showResults: false});
    }

    render() {
        let resultsClass = 'search-bar-results ';
        if (this.state.showResults) {
            resultsClass += 'results-show ';
        }

        if (this.props.searchResults.length === 0) {
            resultsClass += 'results-empty '
        }

        return (
            <div id="user-search-top" className="search-bar user-search">
                <input placeholder="Search User" onChange={(e) => this._onSearchInputChange(e)} value={this.state.searchInputValue} type="text" name="user_search" className="search-bar-input"/>
                <div className={resultsClass}>
                    {this._renderSearchResults()}
                </div>
                {this.state.showResults &&
                <div className="modal-bg in-container" onClick={() => this._onOutsideClick()} ref={(el) => this.modal = el}>
                </div>
                }
            </div>
        );
    }

}

UserSearch.propTypes = {
    searchResults: React.PropTypes.arrayOf(React.PropTypes.object),
    startSearch: React.PropTypes.func,
    searchStatus: React.PropTypes.string,
    addUser: React.PropTypes.func
};

UserSearch.defaultProps = {
    searchResults: [],
    startSearch: () => {},
    addUser: () => {},
    searchStatus: FETCH_STATUS.SUCCESS
};

UserSearch.displayName = 'UserSearch';

/*CONTAINER COMPONENT*/
const mapStateToProps = (state, ownProps) => {
    return {
        searchResults: state.userSearchResults,
        searchStatus: state.userSearchStatus
    }
};

const mapDispatchToProps = (dispatch, ownProps) => {
    return {
        startSearch: (query) => dispatch(fetchUserSearchResults(query)),
        addUser: (username) => dispatch(trackUser(username))
    };
};

export const SmartUserSearch = connect(
    mapStateToProps,
    mapDispatchToProps
)(UserSearch);