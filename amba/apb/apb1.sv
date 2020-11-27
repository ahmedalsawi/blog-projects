module top;

   parameter ADDER_SIZE = 12;
   
    logic PCLK;
    logic PRESETn;
    logic [ADDER_SIZE-1:0] PADDR;
     logic PWRITE;
        logic PSELx;
     logic PENABLE;
     logic [31:0] PWDATA; 
     logic [31:0] PRDATA; 
    logic PREADY;
 


    master m(.*);
    slave s(.*);


    initial begin
        PCLK= 0;
        forever begin
            #5;
            PCLK= ~PCLK;
        end
    end
    initial begin
        PRESETn = 0;
        repeat(3) @(posedge PCLK);
        PRESETn = 1;
    end
    initial begin
    #100 $finish();
    end
    initial begin
        $monitor( "%t PCLK=%b, PRESETn=%b, PADDR=%x, PWRITE=%b, PSELx=%x, PENABLE=%b,PWDATA=%x, PRDATA=%x,PREADY=%b" ,$time, PCLK, PRESETn, PADDR, PWRITE, PSELx, PENABLE,PWDATA, PRDATA,PREADY);

$dumpvars;
    end
endmodule

module master#(
    parameter ADDER_SIZE = 12
)(
    input logic PCLK,
    input logic PRESETn,

    output logic [ADDER_SIZE-1:0] PADDR,
    output logic PWRITE,
    output logic PSELx,
    output logic PENABLE,
    output logic [31:0] PWDATA,
    input logic [31:0] PRDATA,
    input logic PREADY
);
initial begin
    @(posedge PRESETn);
    @(posedge PCLK);
    #1 PSELx = 1;
    PADDR  = 0;
    PWRITE = 1;
    PWDATA = 2;
    @(posedge PCLK);
    #1 PENABLE = 1;
    @(posedge PCLK);
    while(PREADY==0) begin
        @(posedge PCLK);
    end
    #1 PSELx = 0;
    PENABLE = 0;
end

endmodule

module slave#(
    parameter ADDER_SIZE = 12
)(
    input logic PCLK,
    input logic PRESETn,

    input logic [ADDER_SIZE-1:0] PADDR,
    input logic PWRITE,
    input logic PSELx,
    input logic PENABLE,
    input logic [31:0] PWDATA,
    output logic [31:0] PRDATA,
    output logic PREADY
);


logic [3:0] state, state_n;
parameter IDLE = 0;


// internal ready flag
logic ready=0;
initial begin
#80 ready = 1;
end
logic pready;

assign PREADY = pready;

always @(posedge PCLK) begin
    if (PRESETn == 0 ) begin
        pready <= #1 1'b1;
    end
    else begin
        if (PSELx == 1)  begin
            if(ready == 1) begin
                pready <= #1 1;
            end
            else begin
                pready <= #1 0;
            end
        end
    end
end

always @(posedge PCLK) begin
    if (pready && PENABLE) begin
    $display($time,, "DATA ADDR=%x, DATA=%x", PADDR, PWDATA);
    end
end



endmodule