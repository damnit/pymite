_pymite_completion() {
    COMPREPLY=( $( COMP_WORDS="${COMP_WORDS[*]}" \
                   COMP_CWORD=$COMP_CWORD \
                   _PYMITE_COMPLETE=complete $1 ) )
    return 0
}

complete -F _pymite_completion -o default pymite;
