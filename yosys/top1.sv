module top(input CLK, input RST, input load, input [3:0] in1, output [3:0] out1);
    counter l(CLK, RST, load, in1, out1);
endmodule

module counter(input CLK, input RST, input load,input [3:0] in1, output [3:0] out1);

    reg [3:0] state;
    always @(posedge CLK) begin
        if (RST == 0)
            state <= 0;
        else if (load==1) begin
            state <= in1;
        end
        else begin   
            state <= state +1;
        end
    end

    assign out1 = state;
endmodule