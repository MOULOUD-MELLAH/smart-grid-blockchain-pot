# solidity string utilities.

Simplify dumping data as string in solidity.

Optimized for usability, and not for gas.

Mostly useful in testing by generating meaningful revert messages.

Currently supports `toString()` method for `uint`, `address`, `bytes32`, `bool`, `int` and `string`

Also provides `concat()` methods for those types, but only with 2 and 3 params.
For longer params, use multiple `concat` calls or `abi.encodePacked()`

e.g.

```solidity
import "solidity-string-utils/StringUtils.sol";

contract MyContract {

    using StringUtils for *;

    function someMethod() public {


        require(condition, "condition not met"
            .concat( " a=", a)
            .concat( " b=", b)
        );

        revert(string(abi.encodePacked(
                "asd",
                a.toString(),
                b.toString(),
                c.toString(),
                d.toString(),
                e.toString()
            )));
    }

}
```

