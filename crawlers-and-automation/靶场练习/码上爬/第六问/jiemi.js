
// text='361d3626adcf4a361c385c8f0b39c963f0469b9c6ff6d23c7e0b145e1b885851be1cff3c2d5ef470376708d6f60fad1c4c9987e181d330ca77dc5cb91d0ab5c1680f095d61499b9023658e14181dee9f1345ad91df727ce58e869da5f59aef9df7f38b4730811ba0fe75bd3c2c95fdd5054eb1e57ee01817f2ade931100f307b497bc2b6dade4143419d9613f268f80283cdf202aba59e969fd8e4338e9678f4d5301e80407904687f5e0c68d4ba413d0a66dbc4f2758901aa4ff102be1b31aeea6d53acc884ea1abf6dba04fd8b9582027caf80badcefa2df46b1076ff883ed99aa1acd9860c7050a9e4ea36493a5b9f26ea29bd1bc5378f881856e9648ad3e977a57d33ffab33a406087a34ba40abd66859bb0f0328978c5ad97b43f3d8142724f9f051f4b276ec253da7fd33b0a3b66e900ba30f749420f402d178d77994097279565ce7630f5840ec5a5754fce466dfb215b96f9c0a795e844bece955f54e294d71c4e2cd96b92b110392629e1771938ae09d9f7c4c75d47af17d744e13134be19913373c7b6b17de26f68c1777d572120475bd605739dbc48752a502d3c7d766298efa5de14017c586be09b372c558741098361b22ee7f0cbb525267faa67c76d90e769b73d06e402111499e3b3013de5af8a41b3829b49bf5d72845272d2ed431ef8fda40f3f0079b1cadcf2b0'
dd_a=require('crypto-js')
kkkk={
    "words": [
        2021161080,
        2021161080,
        1869573999,
        1869573999
    ],
    "sigBytes": 16
}
iiii={
    "words": [
        808530483,
        875902519,
        943276354,
        1128547654
    ],
    "sigBytes": 16
}
function xxxxoooo(encryptedHex) {
    let enccc = dd_a.enc.Hex.parse(encryptedHex);
    let deccc = dd_a.AES["decr" + "ypt"]({ciphertext: enccc}, kkkk, {
        mode: dd_a.mode.CBC,
        padding: dd_a.pad.Pkcs7,
        iv: iiii,
    });
    return deccc.toString(dd_a.enc.Utf8);
}


// console.log(xxxxoooo(text))

