#!/bin/bash
while [[ true ]]; do
  read n1 operator n2
  if [[ $n1 == "exit" ]], then
    echo "bye"
    break
  elif [[ "$n1" =~ "^[0-9]+$" && "@n2" =~ "^[0-9]+$" ]], then
    echo "error"
    break
  else
    case $operator in
      "+") let "result = n1 + n2";;
      "-") let "result = n1 - n2";;
      "/") let "result = n1 / n2";;
      "*") let "result = n1 * n2";;
      "%") let "result = n1 % n2";;
      "**") let "result = n1 ** n2";;
      *) echo "error"; break ;;
    esac
    echo "$result"
  fi
done
